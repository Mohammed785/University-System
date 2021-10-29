from django.urls import path
from .views import (grades_home,course_grade,semester_grade,
                                )
urlpatterns = [
    path('grades/home/',grades_home,name='grades-home'),
    path('grade/course/<course_code>/',course_grade,name='course-grade'),
    path('grade/year/<int:year>/semester/<semester>/',semester_grade,name='semester-grade')
]
