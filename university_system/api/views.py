from django.shortcuts import render
from django.contrib.auth.models import AnonymousUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import exceptions
from grades.models import Grade
from courses.models import Course
from quizzes.models import Quiz

@api_view(['GET'])
def gradeview(request,course_code):
    if isinstance(request.user,AnonymousUser):
        raise exceptions.NotAuthenticated
    try:
        course = Course.objects.get(course_code=course_code)
        grade = Grade.objects.get(student=request.user,course=course)
    except (Course.DoesNotExist,Grade.DoesNotExist):
        raise exceptions.NotFound
    grades = {
        'Final':grade.final,
        'Quizzes':grade.get_quiz_grades(),
        'Assignament':grade.get_assignament_grades(),
        'Midterm':grade.get_midterm_grades(),
        'Others':grade.other,
        'Total':grade.get_total_grades()
    }
    data = {
        'labels':grades.keys(),
        'data':grades.values(),
        'course':course
    }
    return Response(data=data)

def gradeView(request):
    return render(request,'grade/gradeview.html')

@api_view(['GET'])
def course_quizzes_grade_api(request,course_code):
    if isinstance(request.user,AnonymousUser):
        raise exceptions.NotAuthenticated
    try:
        course = Course.objects.get(course_code=course_code)
        quizzes = Quiz.objects.get_answered_quizzes(course=course,studnet=request.user)
        grades = {quiz.name:Quiz.objects.get_student_grade(quiz,request.user) for quiz in quizzes}
    except (Course.DoesNotExist,Quiz.DoesNotExist):
        raise exceptions.NotFound
    data = {#try to do it in one dict compre
        'labels':grades.keys(),
        'data':grades.values(),
    }
    return Response(data=data)

def course_quizzes_grade_view(request):
    return render(request,'grade/quizgrade.html')

@api_view(['GET'])
def semester_course_grade_api(request):
    ...

def semester_course_grade_view(request):
    return render(request,'grade/semester_grade.html')