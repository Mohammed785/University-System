from django.urls import path
from .views import (
    courses_list,course_view,download_file,course_announcements,course_assignments,assignment_update,announcement_update,
    delete_announcement,delete_assignment,delete_course_file,course_files_view,course_questions,delete_question,delete_answer,
    question_update
)


urlpatterns = [
    path("courses/", courses_list, name="courses-list"),
    path("course/<course_code>/", course_view, name="course-view"),
    path("course/<course_code>/questions/", course_questions, name="course-questions"),
    path("course/<course_code>/announcements/", course_announcements, name="course-announcements"),
    path("course/<course_code>/assignments/", course_assignments, name="course-assignments"),
    path('course/assignment/<slug:slug>/update/',assignment_update,name='assignment-update'),
    path("course/announcement/<slug:slug>/update/",announcement_update,name='announcement-update'),
    path("course/question/<slug:slug>/update/",question_update,name='question-update'),
    path("course/announcement/<slug:slug>/delete/", delete_announcement, name="delete-announcement"),
    path("course/assignment/<slug:slug>/delete/", delete_assignment, name="delete-assignment"),
    path("course/file/<slug:slug>/delete/", delete_course_file, name="delete-course-file"),
    path('course/question/<slug:slug>/delete/',delete_question,name='delete-question'),
    path('course/answer/<slug:slug>/delete/',delete_answer,name='delete-answer'),
    path("course/<course_code>/files/", course_files_view, name="course-files"),
    path("download/<filepath>/", download_file, name="download-file"),
]
