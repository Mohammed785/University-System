from django import forms
from .models import Quiz, QuizQuestion, QuizQuestionChoices, StudentQuizAnswers, QuizAttempts
from grades.models import QuizGrade, Grade, Year
from users.utils import get_current_year


class AnswerQuizForm(forms.Form):
    def __init__(self, questions, data=None, user=None, *args, **kwargs):
        super(AnswerQuizForm, self).__init__(data, *args, **kwargs)
        self.user = user
        self.questions = questions
        for question in questions:
            field_name = f"{question.pk}"
            choices = [(answer, answer.body) for answer in question.choices.all()]
            self.fields[field_name] = forms.ChoiceField(label=question.body, choices=choices, widget=forms.RadioSelect)
        return None

    def save(self):
        year, _ = Year.objects.get_or_create(year=get_current_year())

        grade, _ = Grade.objects.get_or_create(student=self.user, course=self.questions.first().quiz.course, year=year)

        quiz_grade, _ = QuizGrade.objects.get_or_create(
            quiz=self.questions.first().quiz,
            student=self.user,
            grade=grade,
            course=self.questions.first().quiz.course,
            year=year,
        )
        for ans in self.cleaned_data:
            question = QuizQuestion.objects.get(pk=int(ans))
            choice = QuizQuestionChoices.objects.filter(body=self.cleaned_data[ans]).first()
            answer = StudentQuizAnswers(student=self.user, quiz=question.quiz, question=question, choice=choice)
            answer.save()
            if answer.is_right:
                quiz_grade.mark += question.grade
        quiz_grade.save()
        attemp = QuizAttempts(students=self.user)
        return attemp


class CreateQuizForm(forms.ModelForm):
    start = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))

    class Meta:
        model = Quiz
        fields = ["name", "start", "duration"]


class CreateQuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ["body", "grade"]


class CreateQuizQuestionChoices(forms.ModelForm):
    class Meta:
        model = QuizQuestionChoices
        fields = ["body", "is_correct"]
