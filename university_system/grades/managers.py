from django.db import models
from users.models import User
from courses.models import Course
from quizzes.models import Quiz
from users.decorators import try_expect

class GradeManager(models.Manager):
    def grade_search_logic(self, course, year):
        from .models import Year
        from courses.models import Course

        year = Year.objects.get(year=year)
        course = Course.objects.get(course_code=course)
        return year, course

    def get_passed_grade(self, course, grade, year):
        g_year, g_course = self.grade_search_logic(course, year)
        results = self.filter(final__gt=grade, course=g_course, year=g_year)
        return results, results.count()

    def get_un_passed_grade(self, course, grade, year):
        g_year, g_course = self.grade_search_logic(course, year)
        results = self.filter(final__lt=grade, course=g_course, year=g_year)
        return results, results.count()

    def get_avg_course_grades(self, course, year):
        year, course = self.grade_search_logic(course, year)
        grades = self.filter(year=year, course=course).all()
        grades_count = grades.count() if grades.count()>0 else 1
        grades_sum = sum([instacne.get_total_grades() for instacne in grades])
        return grades_sum / grades_count, grades_count, grades_sum

    def get_student_grades(self, student_id, year):
        from grades.models import Year

        student = User.objects.get(college_id=student_id)
        year = Year.objects.get(year=year)
        grades = self.filter(student=student, year=year).all()
        return grades


class SemesterGradesManager(models.Manager):
    def search_sem_year(self, semester, year):
        from .models import Semester, Year

        year = Year.objects.get(year=year)
        semester = Semester.objects.get(semester=semester, year=year)
        return year, semester

    def get_student_semester_grades(self, student_id, semester, year):
        year, semester = self.search_sem_year(semester, year)
        student = User.objects.get(college_id=student_id)
        semester_grade = self.filter(year=year, semester=semester, student=student).first()
        return {"name": student.name, "total": semester_grade.calc_total()[-1], "gpa": semester_grade.calc_gpa()}

    def get_semester_grades_avg(self, semester, year):
        year, semester = self.search_sem_year(semester, year)
        grades = self.filter(year=year, semester=semester).all()
        grades_count = grades.count() if grades.count()>0 else 1
        grades_sum = sum(grade.calc_total()[-1] for grade in grades)
        gpa_total = sum(grade.calc_gpa() for grade in grades)
        return {"grade_avg": grades_sum / grades_count, "gpa_avg": gpa_total / grades_count, "count": grades_count}


class MidtermGradeManager(models.Manager):
    def search_logic(self, course_code, semester, year):
        from .models import Year, Semester

        course = Course.objects.get(course_code=course_code)
        year = Year.objects.get(year=year)
        semester = Semester.objects.get(semester=semester, year=year)
        return course, year, semester

    def get_grades_gt(self, course_code, semester, year, mark):
        course, year, semester = self.search_logic(course_code, semester, year)
        return self.filter(course=course, year=year, semester=semester, mark__gt=mark).all()

    def get_grades_lt(self, course_code, semester, year, mark):
        course, year, semester = self.search_logic(course_code, semester, year)
        return self.filter(course=course, year=year, semester=semester, mark__lt=mark).all()

    def get_grades_avg(self, course_code, semester, year):
        course, year, semester = self.search_logic(course_code, semester, year)
        grades = self.filter(course, course, year=year, semester=semester).all()
        grades_count = grades.count() if grades.count()>0 else 1
        grades_sum = sum(grade.mark for grade in grades)
        return grades_sum / grades_count, grades_count


class QuizGradeManager(models.Manager):
    def get_quiz_avg(self, quiz_slug):
        quiz = Quiz.objects.get(slug=quiz_slug)
        grades = self.filter(quiz=quiz).all()
        grades_count = grades.count() if grades.count()>0 else 1
        grades_sum = sum(grade.mark for grade in grades)
        return (grades_sum / grades_count, grades_count, quiz.name, grades_sum)

    def get_course_avg(self, course_code, year):
        from grades.models import Year

        course = Course.objects.get(course_code=course_code)
        year = Year.objects.get(year=year)
        grades = self.filter(course=course, year=year).all()
        quizzes = set(grade.quiz.slug for grade in grades)
        count = len(quizzes) if len(quizzes)>0 else 1
        return sum(self.get_quiz_avg(slug)[-1] for slug in quizzes) / count

    def get_grades_under(self, quiz_slug, grade):
        quiz = Quiz.objects.filter(slug=quiz_slug).first()
        return self.filter(quiz=quiz, course=quiz.course, mark__lt=grade).all()

    def get_grades_passes(self, quiz_slug, grade):
        quiz = Quiz.objects.filter(slug=quiz_slug).first()
        return self.filter(quiz=quiz, course=quiz.course, mark__gt=grade).all()
