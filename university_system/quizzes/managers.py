from django.db import models



class QuizManager(models.Manager):

    def get_opened_quizzes(self,course):
        quizzes = self.filter(course=course).all()
        return [quiz for quiz in quizzes if quiz.is_open]


    def get_closed_quizzes(self,course):
        quizzes = self.filter(course=course).all()
        return [quiz for quiz in quizzes if not quiz.is_open]

    #Re check answered an unanswered
    def get_answered_quizzes(self,course,studnet):
        from .models import QuizAttempts
        student_attempts = QuizAttempts.objects.filter(student=studnet).all()
        quizzes = self.filter(course=course,students_attempts__in=student_attempts).all()
        return quizzes,course

    def get_unanswered_quizzes(self,course,studnet):
        quizzes = self.filter(course=course).all()
        answered= self.get_answered_quizzes(course,studnet)
        return [quiz for quiz in quizzes if quiz not in answered]