from django.urls import path
from .views import (
    create_question_choice,create_quiz,create_quiz_question,show_course_quizzes,UpdateChoiceView,
    UpdateQuestionView,UpdateQuizView,DeleteChoiceView,DeleteQuestionView,
    DeleteQuizView,take_quiz_view,quiz_answer_view,review_quiz_view,
)

urlpatterns = [
    path("quiz/<slug:slug>/create/", create_quiz, name="create-quiz"),
    path("quiz/<slug:slug>/question/create/", create_quiz_question, name="create-quiz-question"),
    path("question/<slug:slug>/choice/create/", create_question_choice, name="create-q-choice"),
    path("quiz/<slug:slug>/update/", UpdateQuizView.as_view(template_name="quiz/update_quiz.html"), name="quiz-update"),
    path("quiz/<slug:slug>/delete/", DeleteQuizView.as_view(template_name="quiz/delete_quiz.html"), name="quiz-delete"),
    path("quiz/<slug>/", take_quiz_view, name="quiz-view"),
    path("quiz/<slug:slug>/answers/", quiz_answer_view, name="quiz-answers-view"),
    path("quiz/<slug>/review", review_quiz_view, name="quiz-review"),
    path("course/<slug:slug>/quizzes/",show_course_quizzes,name="course-quizzes"),
    path(
        "question/<slug:slug>/update/",
        UpdateQuestionView.as_view(template_name="quiz/update_question.html"),
        name="quiz-q-update"
    ),
    path(
        "question/<slug:slug>/delete/",
        DeleteQuestionView.as_view(template_name="quiz/delete_question.html"),
        name="quiz-q-delete"
    ),
    path(
        "choice/<slug:slug>/update/",
        UpdateChoiceView.as_view(template_name="quiz/choice_update.html"),
        name="question-c-update"
    ),
    path(
        "choice/<slug:slug>/delete/",
        DeleteChoiceView.as_view(template_name="quiz/choice_delete.html"),
        name="question-c-delete"
    )
]
