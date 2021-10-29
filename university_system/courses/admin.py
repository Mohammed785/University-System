from django.contrib import admin
from .models import Course, Announcement, Assignment, CourseFiles, Questions, Answers


admin.site.register(Course)
admin.site.register(Announcement)
admin.site.register(Assignment)
admin.site.register(CourseFiles)
admin.site.register(Questions)
admin.site.register(Answers)
