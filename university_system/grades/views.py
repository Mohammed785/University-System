from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from courses.models import Course
from .models import Year, Semester
from datetime import datetime


@login_required
def grades_home(request):
    courses = Course.objects.filter(students__id=request.user.id).all()
    return render(request, "grade/home.html",context={"courses":courses})


@login_required
def course_grade(request, course_code):
    course = get_object_or_404(Course, course_code=course_code)
    year = get_object_or_404(Year, year=datetime.now().year)
    return render(request, "grade/course_grades.html", context={"course": course, "year": year})


@login_required
def semester_grade(request, year, semester):
    year = get_object_or_404(Year, year=year)
    semester = get_object_or_404(Semester, semester=semester)
    return render(request, "grade/semester_grade.html", context={"year": year, "semester": semester})
