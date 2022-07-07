from django.db import models


class QuizManager(models.Manager):
    def get_opened_quizzes(self, course):
        quizzes = self.filter(course=course).all()
        return [quiz for quiz in quizzes if quiz.is_open]

    def get_closed_quizzes(self, course):
        quizzes = self.filter(course=course).all()
        return [quiz for quiz in quizzes if not quiz.is_open]

    def get_answered_quizzes(self, course, student):
        from .models import QuizAttempts

        student_attempts = QuizAttempts.objects.filter(students=student).all()
        quizzes = self.filter(course=course, students_attempts__in=student_attempts).all()
        return quizzes

    def get_unanswered_quizzes(self, course, student):
        quizzes = self.filter(course=course).all()
        answered = self.get_answered_quizzes(course, student)
        return [quiz for quiz in quizzes if quiz not in answered]

    def get_student_grade(self, quiz, student):
        from .models import StudentQuizAnswers

        answers = StudentQuizAnswers.objects.filter(student=student, quiz=quiz).all()
        return sum(ans.get_grade() for ans in answers)
