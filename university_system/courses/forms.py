from django import forms
from .models import Course, Announcement, Assignment, CourseFiles, Questions, Answers


class AssignmentForm(forms.ModelForm):
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))

    class Meta:
        model = Assignment
        fields = ["name", "file", "max_mark", "deadline", "notes"]


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["body", "public"]


class CourseFilesForm(forms.ModelForm):
    class Meta:
        model = CourseFiles
        fields = ["name", "file"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ["body"]


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answers
        fields = ["body"]
