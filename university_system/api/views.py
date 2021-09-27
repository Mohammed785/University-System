from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from grades.models import Grade
from courses.models import Course

@api_view(['GET'])
def gradeview(request,course_code):
    # student_id = request.query_params.get('id')
    course = Course.objects.get(course_code=course_code)
    grade = Grade.objects.get(student=request.user,course=course)
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
        'data':grades.values()
    }
    return Response(data=data)

def gradeView(request):
    return render(request,'grade/gradeview.html')