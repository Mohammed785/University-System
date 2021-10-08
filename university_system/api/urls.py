from django.urls import path
from .views import (gradeview,gradeView,course_quizzes_grade_api,course_quizzes_grade_view
                                ,semester_course_grade_api,semester_course_grade_view,midterm_grade,midterm_grade_api,
                                year_midterm_api,course_data_api,announcement_detail_api,quiz_grade_search_api,
                                assignment_detail_api,quiz_data_api,quiz_grades_detail_api,course_quizzes_detail,
                                midterm_grade_search_api,student_semester_grade_api,students_semester_grade_detail_api,
                                grades_search_api,course_grades_detail_api,get_student_grades,check_quiz_time_api)

urlpatterns = [
    path('grade/api/<course_code>/',gradeview,name='api-grade-view'),
    path('grade/',gradeView,name='grade-view'),
    path('grade/quizzes/api/<course_code>',course_quizzes_grade_api,name='quizzes-api'),
    path('grade/quizzes/',course_quizzes_grade_view,name='quizzes-view'),
    path('grade/semester/api/<int:year>/<semester>/',semester_course_grade_api,name='semester-grade-api'),
    path('grade/semester/',semester_course_grade_view,name='semester-grade-view'),
    path('grade/midterm/<int:year>/<semester>/',midterm_grade_api,name='midterm-grade-api'),
    path('grade/midterm/',midterm_grade,name='midterm_grade'),
    path('api/<int:year>/',year_midterm_api,name='year-midterms'),
    path('api/course/<code>/',course_data_api,name='course-detail'),
    path('announcement/<slug:slug>/detail/',announcement_detail_api,name='announcement-detail'),
    path('assignment/<slug:slug>/detail/',assignment_detail_api,name='assignment-detail'),
    path('quiz/<slug:slug>/detail/',quiz_data_api,name='quiz-detail'),
    path('quiz/grades/<slug:slug>/detail/',quiz_grades_detail_api,name='quiz-grades-detail'),
    path('quiz/course/<course_code>/<int:year>/grades/detail/',course_quizzes_detail,name='course-quizzes-grade-detail'),
    path('quiz/<slug:slug>/<int:mark>/<type>/search/',quiz_grade_search_api,name='quiz-grade-search-api'),
    path('course/<course_code>/<semester>/<int:year>/midterm/<int:mark>/<type>/',midterm_grade_search_api,name='midterm-grade-search'),
    path('grade/student/<college_id>/semester/<semester>/<int:year>/detail/',student_semester_grade_api,name='semester-course-grade'),
    path('grade/semester/<semester>/<int:year>/detail/',students_semester_grade_detail_api,name='grade-semester-detail'),
    path('grade/<course_code>/<int:grade>/<int:year>/<type>/search/',grades_search_api,name='grades-year-search'),
    path('grade/course/<course>/<int:year>/detail/',course_grades_detail_api,name='course-grade-detail'),
    path('student/grades/<student_id>/<int:year>/detail',get_student_grades,name='student-grades-detail'),
    path('quiz/<slug:slug>/time/',check_quiz_time_api,name='check-quiz-time')
]