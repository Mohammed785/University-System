from rest_framework import serializers
from courses.models import Course,Assignment,Announcement,Questions,Answers
from grades.models import QuizGrade,Grade,SemesterGrade,MidtermGrade,AssignmentGrade
from quizzes.models import Quiz,QuizQuestion,QuizQuestionChoices


class CourseSerializer(serializers.ModelSerializer):
    professor=serializers.StringRelatedField(many=True)
    students=serializers.StringRelatedField(many=True)
    assignments = serializers.HyperlinkedRelatedField(view_name='assignment-detail',read_only=True,many=True,lookup_field='slug')
    quizzes = serializers.HyperlinkedRelatedField(view_name='quiz-detail',read_only=True,many=True,lookup_field='slug')
    announcements = serializers.HyperlinkedRelatedField(view_name='announcement-detail',read_only=True,many=True,lookup_field='slug')
    class Meta:
        model = Course
        fields = ['name','course_code','descreption','professor','students','quizzes','assignments','announcements']

class SemesterGradeSerializer(serializers.ModelSerializer):
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

class QuizQuestionChoiceSerializer(serializers.ModelSerializer):
    chosen = serializers.SerializerMethodField('get_count')
    class Meta:
        model = QuizQuestionChoices
        fields= ['body','is_correct','chosen']

    def get_count(self,obj):
        return obj.get_count
class QuizQuestionSerializer(serializers.ModelSerializer):
    choices = QuizQuestionChoiceSerializer(many=True,read_only=True)
    class Meta:
        model = QuizQuestion
        fields = ['body','grade','choices']

class QuizSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(format='%m/%d/%Y, %H:%M')
    course = serializers.StringRelatedField()
    prof = serializers.StringRelatedField()
    open = serializers.SerializerMethodField('is_open')
    end_time = serializers.SerializerMethodField('get_end_time')
    total_grade = serializers.SerializerMethodField('get_quiz_grade')
    attempts = serializers.SerializerMethodField('get_attempts_count')
    questions = QuizQuestionSerializer(many=True,read_only=True)
    class Meta:
        model = Quiz
        fields = ['name','start','duration','end_time','open','total_grade','attempts','course','prof','questions']
    
    def is_open(self,obj):
        return obj.is_open

    def get_end_time(self,obj):
        endtime=obj.get_end_time
        return endtime.strftime('%m/%d/%Y, %H:%M')

    def get_quiz_grade(self,obj):
        return obj.get_quiz_grade

    def get_attempts_count(self,obj):
        return obj.students_attempts.count()

class AssignmentSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    professor = serializers.StringRelatedField()
    deadline = serializers.DateTimeField(format='%m/%d/%Y, %H:%M')
    upload_date = serializers.DateTimeField(format='%m/%d/%Y, %H:%M')
    class Meta:
        model = Assignment
        fields = ['deadline','max_mark','notes','upload_date','professor','course','slug']
class AnnouncementSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    date_posted = serializers.DateTimeField(format='%m/%d/%Y, %H:%M')
    course = serializers.StringRelatedField()
    class Meta:
        model = Announcement
        fields = ['body','date_posted','author','course','public']

class MidtermGradeSerializer(serializers.ModelSerializer):
    year = serializers.StringRelatedField()
    course = serializers.StringRelatedField()
    student = serializers.StringRelatedField()
    semester = serializers.StringRelatedField()
    class Meta:
        model = MidtermGrade
        fields = ['mark','year','course','student','semester']

class AssignmentGradeSerializer(serializers.ModelSerializer):
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


class GradeSerializer(serializers.ModelSerializer):
    midterm = MidtermGradeSerializer(many=True,read_only=True)
    assignment = AssignmentGradeSerializer(many=True,read_only=True)
    quiz = QuizGradeSerializer(many=True,read_only=True)
    student = serializers.StringRelatedField()
    course = serializers.StringRelatedField()
    year = serializers.StringRelatedField()
    class Meta:
        model = Grade
        fields = ['final','other','student','course','year','midterm','assignment','quiz']


class AnswersSerializer(serializers.ModelSerializer):
    date_posted = serializers.DateTimeField(format='%m/%d/%Y, %H:%M')
    author = serializers.StringRelatedField()
    question = serializers.StringRelatedField()
    class Meta:
        model = Answers
        fields = ['body','edited','date_posted','author','question']

class QuestionsSerializer(serializers.ModelSerializer):
    date_posted = serializers.DateTimeField(format='%m/%d/%Y, %H:%M')
    author = serializers.StringRelatedField()
    course = serializers.StringRelatedField()
    answers = AnswersSerializer(many=True,read_only=True)
    class Meta:
        model = Questions
        fields = ['body','edited','date_posted','course','author','answers']