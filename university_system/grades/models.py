from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course, Assignment
from quizzes.models import Quiz
from datetime import date
from .managers import GradeManager, MidtermGradeManager, SemesterGradesManager, QuizGradeManager

User = get_user_model()


SEMESTER_CHOICES = [("1ST", "First"), ("2ND", "Second")]

YEARS = [(y, y) for y in range(2000, date.today().year + 1)]


class Year(models.Model):
    year = models.PositiveSmallIntegerField(choices=YEARS, unique=True)

    def __str__(self):
        return f"{self.year}"


class Semester(models.Model):
    semester = models.CharField(choices=SEMESTER_CHOICES, max_length=3)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["semester", "year"], name="unique_year")]

    def __str__(self):
        return f"{self.semester},{self.year}"


class Grade(models.Model):
    final = models.PositiveSmallIntegerField(default=0)
    other = models.PositiveSmallIntegerField(default=0)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name="course_grade")
    semester_grade = models.ForeignKey(
        "SemesterGrade", on_delete=models.CASCADE, null=True, blank=True, related_name="course_grade"
    )
    objects = GradeManager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["year", "course", "student"], name="year_grade")]

    def __str__(self):
        return f"{self.course.name}/student:{self.student.email} Grade"

    def get_quiz_grades(self):
        total = 0
        for quiz in self.quiz.all():
            total += quiz.mark
        return total

    def get_assignment_grades(self):
        total = 0
        for assin in self.assignment.all():
            total += assin.mark
        return total

    def get_midterm_grades(self):
        total = 0
        for mid in self.midterm.all():
            total += mid.mark
        return total

    def get_total_grades(self):
        return (
            self.get_midterm_grades() + self.final + self.get_quiz_grades() + self.get_assignment_grades() + self.other
        )


class SemesterGrade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    objects = SemesterGradesManager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["year", "student", "semester"], name="year_semsiters")]

    def __str__(self):
        return f"{self.year}:{self.semester}:{self.student.name}"

    def calc_gpa(self):
        return 0.0

    def calc_total(self):
        grades = {course: course.get_total_grades() for course in self.course_grade.all()}
        total = sum(grades.values())
        return (grades, total)


class MidtermGrade(models.Model):
    mark = models.PositiveSmallIntegerField(default=0)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name="midterm")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="midterm")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="midterm")
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="midterm")
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="midterm", limit_choices_to={"is_prof": False}
    )
    objects = MidtermGradeManager()

    def __str__(self):
        return f"{self.student.college_id}:{self.semester}:{self.year}"


class AssignmentGrade(models.Model):
    mark = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="mark")
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"is_prof": False})
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="assignment")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignment_grade")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["assignment", "student"], name="one_assignment_one_mark")]

    def __str__(self):
        return f"Assignment/{self.student.name}:{self.mark}"


class QuizGrade(models.Model):
    mark = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"is_prof": False})
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="quiz_grade")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quiz_grade")
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="quiz")
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name="quiz_grade")
    objects = QuizGradeManager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["student", "quiz"], name="one_grade")]

    def __str__(self):
        return f"{self.student.college_id} grade:{self.grade}"
