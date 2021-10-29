from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from users.decorators import check_prof_previlage
from .models import Course, Quiz, QuizAttempts, QuizQuestion, QuizQuestionChoices
from .forms import CreateQuizForm, CreateQuizQuestionChoices, CreateQuizQuestionForm, AnswerQuizForm
from grades.models import QuizGrade
from users.utils import delete_check
from itertools import zip_longest


class CourseQuizzesView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Quiz
    template_name = "course/course_quizzes.html"
    context_object_name = "quizzes"
    paginate_by = 10
    order_by = "-start"

    def get_course(self):
        return get_object_or_404(Course, course_code=self.kwargs["course_code"])

    def test_func(self):
        course = self.get_course()
        if not course.check_user_enrollment(self.request.user):
            return False
        return True

    def get_queryset(self):
        course = self.get_course()
        status = self.request.GET.get("status", None)
        op = {
            "opened": Quiz.objects.get_opened_quizzes,
            "closed": Quiz.objects.get_closed_quizzes,
            "answered": Quiz.objects.get_answered_quizzes,
            "unanswered": Quiz.objects.get_unanswered_quizzes,
        }
        quizzes = Quiz.objects.filter(course=course).all()
        return (
            op.get(status.lower())(course)
            if status in ["opened", "closed"]
            else op.get(status.lower())(course, self.request.user)
            if status in ["answered", "unanswered"]
            else quizzes
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = self.get_course()
        context["status"] = self.request.GET.get("status", "All")
        if context["status"].lower() not in ["opened", "closed", "answered", "unanswered", "all"]:
            context["status"] = "Please Enter A Valid Params Default if All"
        return context


def quiz_answer_view(request, slug):
    quiz = get_object_or_404(Quiz, slug=slug)
    if quiz.is_open:
        messages.warning(request, "Quiz didn't Closed Yet")
        return redirect("course-quizzes", course_code=quiz.course.course_code)
    attempt = QuizAttempts.objects.filter(students=request.user, quiz=quiz).first()
    if not attempt:
        messages.warning(request, "You Didn't Answer This Quiz")
    student_answers = attempt.answers.all()
    q_a = list(zip_longest(quiz.questions.all(), student_answers))
    grade = QuizGrade.objects.filter(quiz=quiz, student=request.user).first()
    context = {"quiz": quiz, "answers": student_answers, "qa": q_a, "attempt": attempt, "grade": grade}
    return render(request, "quiz/show_answer.html", context=context)


def review_quiz_view(request, slug):
    quiz = Quiz.objects.get(slug=slug)
    questions = quiz.questions.all()
    choices = [question.choices.all() for question in questions]
    q_a = list(zip(questions, choices))
    avg, count, _, total = QuizGrade.objects.get_quiz_avg(quiz.slug)
    context = {"quiz": quiz, "q_a": q_a, "avg": avg, "count": count, "total": total}
    return render(request, "quiz/review_quiz.html", context=context)


def take_quiz_view(request, slug):
    quiz = get_object_or_404(Quiz, slug=slug)
    attemp = QuizAttempts.objects.filter(quiz=quiz, students=request.user).first()
    if not quiz.is_open:
        messages.info(request, "Quiz Is Closed")
        return redirect("home")
    if attemp:
        messages.info(request, "You Have Already Answered This Quiz")
        return redirect("home")
    form = AnswerQuizForm(questions=quiz.questions.all())
    if request.method == "POST":
        form = AnswerQuizForm(data=request.POST, questions=quiz.questions.all(), user=request.user)
        if form.is_valid():
            attemp = form.save()
            attemp.quiz = quiz
            attemp.save()
            return redirect("course-quizzes", course_code=quiz.course.course_code)
    context = {"quiz": quiz, "form": form}
    return render(request, "quiz/take_quiz.html", context=context)


def create_quiz(request, course_code):
    course = Course.objects.filter(course_code=course_code).first()
    if request.method == "POST":
        form = CreateQuizForm(request.POST)
        quiz = form.save(commit=False)
        quiz.course = course
        quiz.prof = request.user
        quiz.save()
        form.save_m2m()
        return redirect("create-quiz-question", slug=quiz.slug)
    else:
        form = CreateQuizForm()
    context = {"form": form, "course": course}
    return render(request, "quiz/create_quiz.html", context=context)


def create_quiz_question(request, slug):
    quiz = Quiz.objects.filter(slug=slug).first()
    if request.method == "POST":
        form = CreateQuizQuestionForm(request.POST, request.FILES)
        question = form.save(commit=False)
        question.quiz = quiz
        question.save()
        form.save()
        return redirect(question.get_absolute_url())
    else:
        form = CreateQuizQuestionForm()
    context = {"form": form, "quiz": quiz}
    return render(request, "quiz/create_question.html", context=context)


def create_question_choice(request, slug):
    question = QuizQuestion.objects.filter(slug=slug).first()
    if request.method == "POST":
        form = CreateQuizQuestionChoices(request.POST)
        choice = form.save(commit=False)
        if any(choice.is_correct for choice in question.choices.all()) and choice.is_correct:
            messages.error(request, "Question can't have more than one correct answer!!")
            messages.error(
                request, f"Choice ({choice.body}) will be saved but as wrong answer you can change this later."
            )
            choice.is_correct = False
        choice.question = question
        choice.save()
        form.save()
        return redirect("create-q-choice", slug=slug)
    else:
        form = CreateQuizQuestionChoices()
    context = {"form": form, "question": question}
    return render(request, "quiz/create_q_choice.html", context=context)


def update_quiz(request, slug):
    quiz = get_object_or_404(Quiz, slug=slug)
    form = CreateQuizForm(instance=quiz)
    if request.method == "POST":
        form = CreateQuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, "Quiz Updated")
            return redirect("course-quizzes", course_code=quiz.course.course_code)
    context = {"form": form, "quiz": quiz}
    return render(request, "quiz/update_quiz.html", context=context)


def update_question(request, slug):
    question = get_object_or_404(QuizQuestion, slug=slug)
    form = CreateQuizQuestionForm(instance=question)
    if request.method == "POST":
        form = CreateQuizQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "Question Updated")
            return redirect("quiz-review", slug=question.quiz.slug)
    context = {"form": form, "question": question}
    return render(request, "quiz/update_question.html", context=context)


def update_question_choice(request, slug):
    choice = get_object_or_404(QuizQuestionChoices, slug=slug)
    form = CreateQuizQuestionChoices(instance=choice)
    if request.method == "POST":
        form = CreateQuizQuestionChoices(request.POST, instance=choice)
        if form.is_valid():
            form.save()
            messages.success(request, "Choice Updated")
            return redirect("quiz-review", slug=choice.question.quiz.slug)
    context = {"form": form, "choice": choice}
    return render(request, "quiz/choice_update.html", context=context)


@login_required
@check_prof_previlage
def delete_quiz(request, slug):
    quiz = get_object_or_404(Quiz, slug=slug)
    if not delete_check(request, "You Are Not Allowed To Delete This Quiz", quiz.prof):
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    quiz.delete()
    messages.success(request, "Quiz Deleted")
    return redirect("course-quizzes", quiz.course.course_code)


@login_required
@check_prof_previlage
def delete_question(request, slug):
    question = get_object_or_404(QuizQuestion, slug=slug)
    if not delete_check(request, "You Are Not Allowed To Delete This Question", question.quiz.prof):
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    question.delete()
    messages.success(request, "Question Deleted")
    return redirect("quiz-review", slug=question.quiz.slug)


@login_required
@check_prof_previlage
def delete_choice(request, slug):
    choice = get_object_or_404(QuizQuestionChoices, slug=slug)
    if not delete_check(request, "You Are Not Allowed To Delete This Choice", choice.get_author):
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    choice.delete()
    messages.success(request, "Choice Deleted")
    return redirect("quiz-review", slug=choice.question.quiz.slug)
