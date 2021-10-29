from django.db import models
from datetime import datetime


class AssignmentManager(models.Manager):
    def get_course(self, course_code):
        from .models import Course

        return Course.objects.get(course_code=course_code)

    def get_opened_assignments(self, course_code):
        course = self.get_course(course_code)
        return self.filter(course=course, deadline__gt=datetime.utcnow()).all()

    def get_closed_assignments(self, course_code):
        course = self.get_course(course_code)
        return self.filter(course=course, deadline__lt=datetime.utcnow()).all()

    def get_uploaded_before(self, course_code, date):
        course = self.get_course(course_code)
        return self.filter(course=course, upload_date__lt=date).all()

    def get_uploaded_after(self, course_code, date):
        course = self.get_course(course_code)
        return self.filter(course=course, upload_date__gt=date).all()


class AnnouncementManager(models.Manager):
    def get_course(self, course_code):
        from .models import Course

        return Course.objects.get(course_code=course_code)

    def get_all_public(self):
        return self.filter(public=True).all()

    def get_course_announcement(self, course_code):
        course = self.get_course(course_code)
        return self.filter(course=course).all()

    def get_announcement_before(self, course_code, date):
        course = self.get_course(course_code)
        return self.filter(course=course, date_posted__lt=date).all()

    def get_announcement_after(self, course_code, date):
        course = self.get_course(course_code)
        return self.filter(course=course, date_posted__gt=date).all()
