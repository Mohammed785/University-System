from rest_framework import serializers
from courses.models import Course
from grades.models import QuizGrade,Grade,SemesterGrade,MidtermGrade,AssignmentGrade
from quizzes.models import Quiz,QuizAttempts


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id',]