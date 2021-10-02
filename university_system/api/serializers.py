from rest_framework import serializers
from courses.models import Course
from grades.models import QuizGrade,Grade,SemesterGrade,MidtermGrade,AssignmentGrade
from quizzes.models import Quiz


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = []

class SemesterSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField('get_total')
    gpa = serializers.SerializerMethodField('get_gpa')
    semester = serializers.StringRelatedField()
    year = serializers.StringRelatedField()
    class Meta:
        model = SemesterGrade
        fields = ['student','total','gpa','semester','year'] 

    def get_total(self,obj):
        return obj.calc_total()[1]

    def get_gpa(self,obj):
        return obj.calc_gpa()
class QuizSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(format='%m/%d/%Y, %H:%M')
    course = serializers.StringRelatedField()
    prof = serializers.StringRelatedField()
    class Meta:
        model = Quiz
        fields = ['name','start','duration','quiz_image','course','prof']

class MidtermGradeSerializer(serializers.ModelSerializer):
    year = serializers.StringRelatedField()
    course = serializers.StringRelatedField()
    student = serializers.StringRelatedField()
    semester = serializers.StringRelatedField()
    class Meta:
        model = MidtermGrade
        fields = ['mark','year','course','student','semester']

class AssignmentSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    student = serializers.StringRelatedField()
    assignment = serializers.StringRelatedField()
    class Meta:
        model = AssignmentGrade
        fields =['mark','student','course','assignment']

class QuizGradeSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    student = serializers.StringRelatedField()
    quiz = serializers.StringRelatedField()
    class Meta:
        model = QuizGrade
        fields = ['mark','student','course','quiz']
