from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import DeleteView,UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.http import HttpResponse,HttpResponseNotFound
from django.contrib import messages
from .models import Course, Quiz, QuizAttempts, QuizQuestion, QuizQuestionChoices,StudentQuizAnswers
from .forms import CreateQuizForm, CreateQuizQuestionChoices, CreateQuizQuestionForm,AnswerQuizForm
from itertools import zip_longest


def show_course_quizzes(request,slug):
    course = get_object_or_404(Course,slug=slug)
    quizzes = Quiz.objects.filter(course=course).order_by('start_time')
    context = {
        'course':course,
        'quizzes':quizzes
    }
    return render(request,'quiz/course_quizzes.html',context=context)

def quiz_answer_view(request,slug):
    quiz = Quiz.objects.filter(slug=slug).first()
    student_answers = StudentQuizAnswers.objects.filter(quiz=quiz).all()
    attemp = QuizAttempts.objects.get(students=request.user,quiz=quiz)
    q_a = list(zip_longest(quiz.questions.all(),student_answers))
    context = {
        'quiz':quiz,
        'answers':student_answers,
        'qa':q_a,
        'attemp':attemp
    }
    return render(request,'quiz/show_answer.html',context=context)


def review_quiz_view(request,slug):
    quiz = Quiz.objects.get(slug=slug)
    questions = quiz.questions.all()
    choices = [question.choices.all() for question in questions]
    q_a = list(zip(questions,choices))
    context = {
        'quiz':quiz,
        'q_a':q_a
    }
    return render(request,'quiz/review_quiz.html',context=context)


def take_quiz_view(request,slug):
    try:
        quiz = Quiz.objects.get(slug=slug)
        attemp =QuizAttempts.objects.get(quiz=quiz,students=request.user)
    except Quiz.DoesNotExist:
        raise HttpResponseNotFound()
    except QuizAttempts.DoesNotExist:
        attemp = False
    if not quiz.is_open:
        messages.info(request,'Quiz Is Closed')
        return redirect('home')

    if attemp:
        messages.info(request,'You Have Already Answered This Quiz')
        return redirect('home')        
    form = AnswerQuizForm(questions=quiz.questions.all())
    if request.method == 'POST':
        """try to find a way insted of this a way that really help
        when the time end the form auto submit an save his answers"""
        #if not quiz.is_open:return redirect('home')
        form = AnswerQuizForm(data=request.POST,questions=quiz.questions.all(),user=request.user)
        if form.is_valid():
            attemp=form.save()
            attemp.quiz=quiz
            attemp.save()
    context = {
        'quiz': quiz,
        'form': form
    }
    return render(request,'quiz/show.html',context=context)

def create_quiz(request, slug):
    course = Course.objects.filter(slug=slug).first()
    if request.method == 'POST':
        form = CreateQuizForm(request.POST, request.FILES)
        quiz = form.save(commit=False)
        quiz.course = course
        quiz.prof = request.user
        quiz.save()
        form.save_m2m()
    else:
        form = CreateQuizForm()
    context = {
        'form': form,
        'course': course
    }
    return render(request, 'quiz/create.html', context=context)


def create_quiz_question(request, slug):
    quiz = Quiz.objects.filter(slug=slug).first()
    if request.method == 'POST':
        form = CreateQuizQuestionForm(request.POST, request.FILES)
        question = form.save(commit=False)
        question.quiz = quiz
        question.save()
        form.save()
        return redirect(question.get_absolute_url())
    else:
        form = CreateQuizQuestionForm()
    context = {
        'form': form,
        'quiz': quiz
    }
    return render(request, 'quiz/create_question.html', context=context)


def create_question_choice(request, slug):
    question = QuizQuestion.objects.filter(slug=slug).first()
    if request.method == 'POST':
        form = CreateQuizQuestionChoices(request.POST)
        choice = form.save(commit=False)
        if any(choice.is_correct for choice in question.choices.all()) and choice.is_correct:
            messages.error(request,"Question can't have more than one correct answer!!")
            messages.error(request,f'Choice ({choice.body}) will be saved but as wrong answer you can change this later.')
            choice.is_correct = False
        choice.question = question
        choice.save()
        form.save()
        return redirect('create-q-choice', slug=slug)
    else:
        form = CreateQuizQuestionChoices()
    context = {
        'form': form,
        'question': question
    }
    return render(request, 'quiz/create_q_choice.html', context=context)


class UpdateQuizView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Quiz
    fields = ['name', 'start', 'course', 'quiz_images']

    def test_func(self):
        quiz = self.get_object()
        if self.request.user != quiz.prof:
            return False
        return True



class UpdateQuestionView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = QuizQuestion
    fields = ['body','grade']

    def test_func(self):
        question = self.get_object()
        if self.request.user != question.get_author:
            return False
        return True


class UpdateChoiceView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = QuizQuestionChoices
    fields = ['body','is_correct']

    def test_func(self):
        choice = self.get_object()
        if self.request.user != choice.get_author:
            return False
        return True


class DeleteQuizView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Quiz
    success_url = 'view-c'

    def test_func(self):
        quiz = self.get_object()
        if self.request.user != quiz.prof:
            return False
        return True


class DeleteQuestionView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = QuizQuestion
    success_url = 'view-c'

    def test_func(self):
        question = self.get_object()
        if self.request.user != question.get_author:
            return False
        return True


class DeleteChoiceView(DeleteView):
    model = QuizQuestionChoices
    success_url = 'view-c'

    def test_func(self):
        choice = self.get_object()
        if self.request.user != choice.get_author:
            return False
        return True

def choice_view(request):
    return HttpResponse('Done Updated')


