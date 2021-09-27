from django.urls import path
from .views import (course_view,create_assignment,create_announcement,download_file,add_course_file,
            ViewCourseAnnouncement,ViewCourseAssignment,UpdateAnnouncementView,UpdateAssignmentView,
            DeleteAnnouncementView,DeleteAssignmentView,DeleteCourseFileView,AnnouncementView,CourseFilesView
)


urlpatterns = [
    path('course/<slug:slug>/', course_view, name='course-view'),
    path('course/<slug:slug>/assignment/create/',create_assignment,name='create-assignment'),
    path('course/<slug:slug>/announcement/create/',create_announcement,name='create-announcement'),
    path('course/<slug:slug>/file/upload/',add_course_file,name='add-course-file'),
    path('download/<filepath>/',download_file,name='download-file'),
    path('announcement/<slug:slug>/',AnnouncementView.as_view(template_name='course/announcement_view.html'),name='announcement-view'),
    path('course/<slug:slug>/announcements/',ViewCourseAnnouncement.as_view(template_name='course/course_announcements.html'),name='course-announcements'),
    path('course/<slug:slug>/assignments/',ViewCourseAssignment.as_view(template_name='course/course_assignments.html'),name='course-assignments'),
    path('announcement/<slug:slug>/update/',UpdateAnnouncementView.as_view(template_name='course/announcement_update.html'),name='update-announcements'),
    path('course/assignment/<slug:slug>/update/',UpdateAssignmentView.as_view(template_name='course/assignment_update.html'),name='update-assignment'),
    path('course/announcement/<slug:slug>/delete/',DeleteAnnouncementView.as_view(template_name='course/announcement_delete.html'),name='delete-announcement'),
    path('course/assignment/<slug:slug>/delete/',DeleteAssignmentView.as_view(template_name='course/assignment_delete.html'),name='delete-assignment'),
    path('course/file/<slug:slug>/delete/',DeleteCourseFileView.as_view(template_name='course/delete_file.html'),name='delete-course-file'),
    path('course/<slug:slug>/files',CourseFilesView.as_view(template_name='course/course_files.html'),name='course-files-view')
]
