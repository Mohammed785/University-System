from django.contrib import admin
from .models import Quiz, QuizQuestion, QuizQuestionChoices, StudentQuizAnswers,QuizAttempts

admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizQuestionChoices)
admin.site.register(StudentQuizAnswers)
admin.site.register(QuizAttempts)