from django import forms
from .models import Course,Announcement,Assignment,CourseFiles


class CreateAssignmentForm(forms.ModelForm):
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))
    class Meta():
        model = Assignment
        fields = ['file','deadline']

class CreateAnnouncementForm(forms.ModelForm):
    class Meta():
        model = Announcement
        fields = ['body']

class CreateCourseFiles(forms.ModelForm):
    class Meta():
        model = CourseFiles
        fields = ['file']
        

