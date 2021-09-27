from django.urls import path
from .views import gradeview,gradeView

urlpatterns = [
    path('grade/api/<course_code>',gradeview,name='api-grade-view'),
    path('grade/',gradeView,name='grade-view')
]