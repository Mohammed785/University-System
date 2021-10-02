from django.urls import path
from .views import (gradeview,gradeView,course_quizzes_grade_api,course_quizzes_grade_view
                                ,semester_course_grade_api,semester_course_grade_view,midterm_grade,midterm_grade_api,
                                year_midterm_api)

urlpatterns = [
    path('grade/api/<course_code>/',gradeview,name='api-grade-view'),
    path('grade/',gradeView,name='grade-view'),
    path('grade/quizzes/api/<course_code>',course_quizzes_grade_api,name='quizzes-api'),
    path('grade/quizzes/',course_quizzes_grade_view,name='quizzes-view'),
    path('grade/semester/api/<int:year>/<semester>/',semester_course_grade_api,name='semester-grade-api'),
    path('grade/semester/',semester_course_grade_view,name='semester-grade-view'),
    path('grade/midterm/<int:year>/<semester>/',midterm_grade_api,name='midterm-grade-api'),
    path('grade/midterm/',midterm_grade,name='midterm_grade'),
    path('api/<int:year>/',year_midterm_api,name='year-midterms')
]