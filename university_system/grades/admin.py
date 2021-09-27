from django.contrib import admin
from .models import Grade,Year,QuizGrade,MidtermGrade,Semester,SemesterGrade,AssignmentGrade


admin.site.register(Grade)
admin.site.register(Year)
admin.site.register(QuizGrade)
admin.site.register(MidtermGrade)
admin.site.register(Semester)
admin.site.register(SemesterGrade)
admin.site.register(AssignmentGrade)

