from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentQuizAnswers,QuizAttempts
from grades.models import QuizGrade


# @receiver(post_save, sender=StudentQuizAnswers)
# def calc_answers(sender, instance, **kwargs):
#     if instance.is_right:
#         grades = QuizGrade.objects.filter(student=instance.student, course=instance.quiz.course).first()
#         if not grades:
#             grades = QuizGrade.objects.create(student=instance.student, course=instance.quiz.course)
#         grades.quizzes += instance.question.grade
#         grades.save()
#     return

# @receiver(post_save,sender=QuizAttempts)
# def save_grade(sender,instance,**kwargs):
#     return QuizGrade.objects.create(student=instance.student,quiz=instance.quiz).save()



# pre_delete for quiz to remove the grade student have

