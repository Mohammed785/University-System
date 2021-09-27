from django.shortcuts import render
from courses.models import Course

def grades_home(request):
    return render(request,'grade/home.html')

def course_grade(request,course_code):#show course pie chart and compare it with other years
    course = Course.objects.get(course_code=course_code)
    return render(request,'grade/course_grade.html',context={'course':course})

def quizzes_grade(request):#show all quizzes grades
    return render(request,'grade/quizzes.html')

def course_quiz_grade(request,course_code):#show course quiz grades
    course = Course.objects.get(course_code=course_code)
    return render(request,'grade/course_quiz_grade',context={'course':course})

def course_assignment_grade(request,course_code):
    course = Course.objects.get(course_code=course_code)
    return render(request,'grade/course_assignment_grade',context={'course':course})

def course_midterm_grade(request,course_code):    
    course = Course.objects.get(course_code=course_code)
    return render(request,'grade/course_midterm_grade',context={'course':course})

def semester_grade(request):#show current semester grade chart and compare it with other semesters//how about show a chart with all courses in this semester
    return render(request,'grade/semester_grade')

def year_grade(request):#show current year chart as pie with two (semesters) and compare it with other years//how about show a chart with all courses in this year
    return render(request,'grade/year_grade')
