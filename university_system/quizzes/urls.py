from django.urls import path
from .views import (
    create_question_choice,create_quiz,create_quiz_question,CourseQuizzesView,update_question_choice,
    update_question,update_quiz,delete_choice,delete_question,
    delete_quiz,take_quiz_view,quiz_answer_view,review_quiz_view,
)

urlpatterns = [
    path("course/<course_code>/quiz/create/", create_quiz, name="create-quiz"),
    path("quiz/<slug:slug>/question/create/", create_quiz_question, name="create-quiz-question"),
    path("question/<slug:slug>/choice/create/", create_question_choice, name="create-q-choice"),
    path("quiz/<slug:slug>/update/", update_quiz, name="quiz-update"),
    path("quiz/<slug>/", take_quiz_view, name="quiz-view"),
    path("quiz/<slug:slug>/answers/", quiz_answer_view, name="quiz-answers-view"),
    path("quiz/<slug:slug>/review/", review_quiz_view, name="quiz-review"),
    path("course/<course_code>/quizzes/",CourseQuizzesView.as_view(),name="course-quizzes"),
    path("question/<slug:slug>/update/",update_question,name="quiz-q-update"),
    path("choice/<slug:slug>/update/",update_question_choice,name="question-c-update"),
    path("question/<slug:slug>/delete/",delete_question,name="quiz-q-delete"),
    path("quiz/<slug:slug>/delete/", delete_quiz, name="quiz-delete"),
    path("choice/<slug:slug>/delete/",delete_choice,name="question-c-delete")
]
