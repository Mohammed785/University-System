from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from users.utils import PathAndRename, slug_generator, image_resize
from courses.models import Course
from datetime import datetime, timedelta
import pytz
from ckeditor_uploader.fields import RichTextUploadingField
from .managers import QuizManager


User = get_user_model()


class Quiz(models.Model):
    name = models.CharField(max_length=30)
    start = models.DateTimeField(null=True)
    duration = models.IntegerField(null=True, blank=True)
    quiz_image = models.ImageField(
        upload_to=PathAndRename("images\\quiz_images"), default="images\\quiz_images\\default.png"
    )
    slug = models.SlugField(max_length=5, null=True, blank=True, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    prof = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={"is_prof": True})
    objects = QuizManager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["name", "course"], name="unique_course")]
        indexes = [models.Index(fields=["slug"], name="quiz_idx")]

    def __str__(self):
        return f"{self.name} {self.course.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_generator(self)
        super().save(*args, **kwargs)
        image_resize(self.quiz_images.path)

    def get_absolute_url(self):
        return reverse("create-quiz-question", kwargs={"slug": self.slug})

    @property
    def get_end_time(self):
        return self.start + timedelta(minutes=self.duration)

    # ERROR TypeError: can't compare offset-naive and offset-aware datetimes

    @property
    def is_open(self):
        if pytz.utc.localize(datetime.utcnow()) > self.get_end_time:
            return False
        return True

    @property
    def get_quiz_grade(self):
        total = 0
        for question in self.questions.all():
            total += question.grade
        return total


class QuizQuestion(models.Model):
    body = RichTextUploadingField(null=True, blank=True)
    grade = models.FloatField(default=0, null=True, blank=True)
    slug = models.SlugField(max_length=5, null=True, blank=True, unique=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")

    class Meta:
        # find a way to handle when user enter non unique values to redirect them to page or show a message insted of logging error
        constraints = [models.UniqueConstraint(fields=["body", "quiz"], name="body_of_the_question")]
        indexes = [models.Index(fields=["slug"], name="question_idx")]

    def __str__(self):
        return f"question:{self.body} quiz:{self.quiz.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_generator(self)

        for token in self.body.split():
            if token.startswith("src="):
                filepath = token.split("=")[1].strip('"')
                filepath = filepath.replace("/media", settings.MEDIA_ROOT)  # don't forget to add PathAndRename
                image_resize(filepath)  # do resize in-place

        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("create-q-choice", kwargs={"slug": self.slug})

    @property
    def get_course(self):
        return self.quiz.course

    @property
    def get_author(self):
        return self.quiz.prof


class QuizQuestionChoices(models.Model):
    body = models.TextField(verbose_name="choice", blank=True, null=True)
    is_correct = models.BooleanField(verbose_name="Correct Answer", default=False)
    slug = models.SlugField(max_length=5, null=True, blank=True, unique=True)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="choices")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["body", "question"], name="non_repeating_choices")]
        indexes = [models.Index(fields=["slug"], name="choice_idx")]

    def __str__(self):
        return f"{self.body}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_generator(self)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):# recheck this i should remove it or change it
        return reverse("view-qs")

    @property
    def get_grade(self):
        return self.question.grade

    @property
    def get_author(self):
        return self.question.get_author


class StudentQuizAnswers(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"is_prof": False})
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE,related_name='student_answers')
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)#i think question and choice should be one to one rel
    choice = models.ForeignKey(QuizQuestionChoices, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["student", "question"], name="one_answer_only")]

    def __str__(self):
        return f"student:{self.student.college_id}//quiz:{self.question.body}"

    @property
    def is_right(self):
        return self.choice.is_correct

    def get_grade(self):
        if self.is_right:
            return self.question.grade
        return 0


class QuizAttempts(models.Model):
    students = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"is_prof": False})
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="students_attempts")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.students.college_id},{self.quiz.name},{self.timestamp}"
