from django.contrib import admin
from .models import (Course, Announcement, Assignment,CourseFiles)


admin.site.register(Course)
admin.site.register(Announcement)
admin.site.register(Assignment)
admin.site.register(CourseFiles)