from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import exceptions
from grades.models import Grade,SemesterGrade,Semester,Year,MidtermGrade,QuizGrade,AssignmentGrade
from courses.models import Course,Assignment,Announcement
from quizzes.models import Quiz
from .serializers import (AnnouncementSerializer, AssignmentGradeSerializer, AssignmentSerializer, 
                                            MidtermGradeSerializer,CourseSerializer, QuizGradeSerializer, 
                                            QuizSerializer, SemesterGradeSerializer,GradeSerializer
                                        )
from users.decorators import check_anonymous,check_prof_previlage

@api_view(['GET'])
@check_anonymous
def gradeview(request,course_code):
    try:
        course = Course.objects.get(course_code=course_code)
        grade = Grade.objects.get(student=request.user,course=course)
        serialized = GradeSerializer(grade)
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
        'grade_data':serialized.data,
        'labels':grades.keys(),
        'data':grades.values(),
        'course':course
    }
    return Response(data=data)

def gradeView(request):
    return render(request,'grade/gradeview.html')

@api_view(['GET'])
@check_anonymous
def course_quizzes_grade_api(request,course_code):
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
@check_anonymous
def semester_course_grade_api(request,year,semester):
    try:
        year=Year.objects.get(year=year)
        semester = Semester.objects.get(semester=semester,year=year)
        grade = SemesterGrade.objects.get(student=request.user,year=year,semester=semester)
        serialized = SemesterGradeSerializer(grade)
    except (Year.DoesNotExist,Semester.DoesNotExist,SemesterGrade.DoesNotExist):
        raise exceptions.NotFound
    grades,total = grade.calc_total()
    labels = [course.course.name for course in grades.keys()]
    data = {
        'semester_grade':serialized.data,
        'labels':labels,
        'data':grades.values(),
        'total':total
    }
    return Response(data=data)
    
def semester_course_grade_view(request):
    return render(request,'grade/semester_grade.html')


@api_view(['GET'])
@check_anonymous
def midterm_grade_api(request,year,semester):
    try:
        year=Year.objects.get(year=year)
        semester = Semester.objects.get(semester=semester,year=year)
        midterm = MidtermGrade.objects.filter(year=year,semester=semester,student=request.user).all()
    except(Year.DoesNotExist,Semester.DoesNotExist,MidtermGrade.DoesNotExist):
        raise exceptions.NotFound
    serialized = MidtermGradeSerializer(midterm)
    grades = {mid.course.name:mid.mark for mid in midterm}
    data = {
        'midterm':serialized.data,
        'labels':grades.keys(),
        'data' : grades.values(),
        'avg':sum(grades.values())/midterm.count()
    }
    return Response(data=data)

def midterm_grade(request):
    return render(request,'grade/midterm_grade.html')

@api_view(['GET'])
@check_anonymous
def year_midterm_api(request,year):
    try:
        year = Year.objects.get(year=year)
        midterm_grades = MidtermGrade.objects.filter(year=year,student=request.user).all()
    except(Year.DoesNotExist,MidtermGrade.DoesNotExist):
        raise exceptions.NotFound
    serializer = MidtermGradeSerializer(instance=midterm_grades,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@check_anonymous
def course_data_api(request,code):
    try:
        course = Course.objects.get(course_code=code)
    except(Course.DoesNotExist):
        raise exceptions.NotFound
    serialized = CourseSerializer(course,context={'request':request})
    return Response(serialized.data)

@api_view(['GET'])
@check_anonymous
def quiz_grade_api(request,quiz_slug):
    try:
        quiz = Quiz.objects.get(slug=quiz_slug)
        quiz_grade = QuizGrade.objects.get(quiz=quiz,student=request.user)
    except (QuizGrade.DoesNotExist,Quiz.DoesNotExist):
        raise exceptions.NotFound
    serialized = QuizGradeSerializer(quiz_grade)
    return Response(serialized.data)

@api_view(['GET'])
@check_anonymous
def assignment_grade_api(request,slug):
    try:
        assignment = Assignment.objects.get(slug=slug)
        assignment_grade = AssignmentGrade.objects.get(assignment=assignment,student=request.user)
    except (Assignment.DoesNotExist,AssignmentGrade.DoesNotExist):
        raise exceptions.NotFound
    serialized = AssignmentGradeSerializer(assignment_grade)
    return Response(serialized.data)
    
@api_view(['GET'])
@check_anonymous
def quiz_data_api(request,slug):
    try:
        quiz = Quiz.objects.get(slug=slug)
    except Quiz.DoesNotExist:
        raise exceptions.NotFound
    serialized = QuizSerializer(quiz)
    return Response(serialized.data)

@api_view(['GET'])
@check_anonymous
def announcement_detail_api(request,slug):
    try:
        announcement = Announcement.objects.get(slug=slug)
    except Announcement.DoesNotExist:
        raise exceptions.NotFound
    serialized = AnnouncementSerializer(announcement)
    return Response(serialized.data)

@api_view(['GET'])
@check_anonymous
def assignment_detail_api(request,slug):
    try:
        assignment = Assignment.objects.get(slug=slug)
    except Assignment.DoesNotExist:
        raise exceptions.NotFound
    serialized = AssignmentSerializer(assignment)
    return Response(serialized.data)

@api_view(['GET'])
@check_anonymous
@check_prof_previlage
def quiz_grades_detail_api(request,slug):
    try:
        avg,count,name,total = QuizGrade.objects.get_quiz_avg(slug)
    except QuizGrade.DoesNotExist:
        raise exceptions.NotFound
    data = {
        'name':name,
        'total':total,
        'avg':avg,
        'count':count
    }
    return Response(data=data)

@api_view(['GET'])
# @check_anonymous
# @check_prof_previlage
def quiz_grade_search_api(request,slug,mark,type):
    try:
        if type.lower()=='greater':
            grades = QuizGrade.objects.get_grades_passes(slug,mark)
        elif type.lower()=='lower':
            grades = QuizGrade.objects.get_grades_under(slug,mark)
        else:raise exceptions.NotAcceptable(detail='Check Your type')
    except QuizGrade.DoesNotExist:
        raise exceptions.NotFound
    serialized = QuizGradeSerializer(grades,many=True)
    return Response(serialized.data)



@api_view(['GET'])
@check_anonymous
@check_prof_previlage
def course_quizzes_detail(request,course_code,year):
    try:
        avg = QuizGrade.objects.get_course_avg(course_code,year)
    except QuizGrade.DoesNotExist:
        raise exceptions.NotFound
    return Response(data={'avg':avg})

@api_view(['GET'])
@check_anonymous
@check_prof_previlage
def midterm_grade_search_api(request,course_code,semester,year,mark,type):
    try:
        if type.lower()=='greater':
            grades = MidtermGrade.objects.get_grades_gt(course_code,semester,year,mark)
        elif type.lower()=='lower':
            grades = MidtermGrade.objects.get_grades_lt(course_code,semester,year,mark)
        else:raise exceptions.NotAcceptable(detail='Check Your type')
    except MidtermGrade.DoesNotExist:
        raise exceptions.NotFound
    data = MidtermGradeSerializer(grades,many=True)
    return Response(data.data)


@api_view(['GET'])
@check_anonymous
@check_prof_previlage
def student_semester_grade_api(request,college_id,semester,year):
    try:
        return Response(SemesterGrade.objects.get_student_semester_grades(college_id,semester,year))
    except(SemesterGrade.DoesNotExist):
        raise exceptions.NotFound


@api_view(['GET'])
@check_anonymous
@check_prof_previlage
def students_semester_grade_detail_api(request,semester,year):
    try:
        return Response(SemesterGrade.objects.get_semester_grades_avg(semester,year))
    except(SemesterGrade.DoesNotExist):
        raise exceptions.NotFound
    

@api_view(['GET'])
@check_anonymous
@check_prof_previlage
def grades_search_api(request,course_code,grade,year,type):
    try:
        if type.lower()=='greater':
            results,count = Grade.objects.get_passed_grade(course_code,grade,year)
        elif type.lower()=='lower':
            results,count = Grade.objects.get_un_passed_grade(course_code,grade,year)
        else:raise exceptions.NotAcceptable(detail='Check Your type')
    except Grade.DoesNotExist:
        raise exceptions.NotFound
    data = {
        'count':count,
        'grades':GradeSerializer(results,many=True).data
    }
    return Response(data)
@api_view(['GET'])
@check_anonymous
@check_prof_previlage
def course_grades_detail_api(request,course,year):
    try:
        avg , count , total = Grade.objects.get_avg_course_grades(course,year)
    except Grade.DoesNotExist:
        raise exceptions.NotFound
    data = {'total':total,'count':count,'avg':avg}
    return Response(data)

@api_view(['GET'])
@check_anonymous
def get_student_grades(request,student_id,year):
    try:
        data = GradeSerializer(Grade.objects.get_student_grades(student_id,year),many=True)
    except Grade.DoesNotExist:
        exceptions.NotFound
    return Response(data.data)

@api_view(['GET'])
@check_anonymous
def check_quiz_time_api(request,slug):
    quiz= Quiz.objects.get(slug=slug)
    return Response(data=quiz.is_open)
