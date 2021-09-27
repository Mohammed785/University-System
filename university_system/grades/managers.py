from django.db import models
from users.models import User
from courses.models import Course
from quizzes.models import Quiz


class GradeManager(models.Manager):
    def grade_search_logic(self, course, year):
        from .models import Year
        from courses.models import Course

        year = Year.objects.filter(year=year).first()
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

    def get_passed_total(self, course, grade, year):
        year, course = self.grade_search_logic(course, year)
        results = [
            instance for instance in self.filter(course=course, year=year) if instance.get_total_grades() >= grade
        ]
        return results, len(results)

    def get_avg_course_grades(self, course, year):
        year, course = self.grade_search_logic(course, year)
        grades = self.filter(year=year, course=course).all()
        grades_count = grades.count()
        grades_sum = sum([instacne.get_total_grades() for instacne in grades])
        return grades_sum / grades_count, grades_count, grades_sum

    def get_precent(self, course, year, grade_to_pass):
        _, all_count, all_sum = self.get_avg_course_grades(course, year)
        results_sum, results_count = self.get_passed_total(course, grade_to_pass, year)
        results_sum = sum(results_sum)
        count_precent = (results_count / all_count) * 100
        grades_precent = (results_sum / all_sum) * 100
        return grades_precent, count_precent

    def get_student_grades(self, student_id):
        student = User.objects.filter(college_id=student_id).first()
        grades = self.filter(student=student).all()
        return grades


class SemesterGradesManager(models.Manager):
    def search_sem_year(self, semester, year):
        from .models import Semester, Year

        year = Year.objects.filter(year=year).first()
        semester = Semester.objects.filter(semester=semester, year=year).first()
        return year, semester

    def get_student_semester_grades(self, student_id, semester, year):
        year, semester = self.search_sem_year(semester, year)
        student = User.objects.filter(college_id=student_id).first()
        semester_grade = self.filter(year=year, semester=semester, student=student).first()
        return semester_grade.calc_total, semester_grade.calc_gpa, semester_grade.grade_set.all()

    def get_semester_grades_avg(self, semester, year):
        year, semester = self.search_sem_year(semester, year)
        grades = self.filter(year=year, semester=semester).all()
        grades_count = grades.count()
        grades_sum = sum(grade.calc_total for grade in grades)
        gpa_avg = sum(grade.calc_gpa for grade in grades)
        return grades_sum / grades_count, gpa_avg / grades_count, grades_count


class MidtermGradeManager(models.Manager):
    def search_logic(self,course_code,semester,year):
        from .models import Year,Semester
        
        course = Course.objects.get(course_code=course_code)
        year = Year.objects.filter(year=year).first()
        semester = Semester.objects.filter(semester=semester,year=year).first()
        return course,year,semester

    def get_grades_gt(self,course_code,semester,year,mark):
        course,year,semester = self.search_logic(course_code,semester,year)
        return self.filter(course=course,year=year,semester=semester,mark__gt=mark).all()

    def get_grades_lt(self,course_code,semester,year,mark):
        course,year,semester = self.search_logic(course_code,semester,year)
        return self.filter(course=course,year=year,semester=semester,mark__lt=mark).all()

    def get_grades_avg(self,course_code,semester,year):
        course,year,semester = self.search_logic(course_code,semester,year)
        grades = self.filter(course,course,year=year,semester=semester).all()
        grades_count = grades.count()
        grades_sum = sum(grade.mark for grade in grades)
        return grades_sum/grades_count,grades_count


class QuizGradeManager(models.Manager):
    def get_quiz_avg(self, quiz_slug):
        quiz = Quiz.objects.filter(slug=quiz_slug).first()
        grades = self.filter(course=quiz.course, quiz=quiz).all()
        grades_count = grades.count()
        grades_sum = sum(grade.mark for grade in grades)
        return (grades_sum / grades_count, grades_count, quiz.name)

    def get_course_avg(self, course_code):
        course = Course.objects.filter(course_code=course_code).first()
        grades = self.filter(course=course).all()
        quizzes = [grade.quiz.slug for grade in grades]
        return [self.get_quiz_avg(course.course_code, slug) for slug in quizzes]

    def get_grades_under(self, quiz_slug, grade):
        quiz = Quiz.objects.filter(slug=quiz_slug).first()
        return self.filter(quiz=quiz, course=quiz.course, mark__lt=grade).all()

    def get_grades_passes(self, quiz_slug, grade):
        quiz = Quiz.objects.filter(slug=quiz_slug).first()
        return self.filter(quiz=quiz, course=quiz.course, mark__gt=grade).all()
