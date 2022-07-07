from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import exceptions, status
from grades.models import Grade, SemesterGrade, Semester, Year, MidtermGrade, QuizGrade, AssignmentGrade
from courses.models import Course, Assignment, Announcement, Answers, Questions
from quizzes.models import Quiz
from .serializers import (
    AnnouncementSerializer,AssignmentGradeSerializer,AssignmentSerializer,MidtermGradeSerializer,AnswersSerializer,
    CourseSerializer,QuizGradeSerializer,QuizSerializer,SemesterGradeSerializer,GradeSerializer,QuestionsSerializer
)
from users.decorators import check_anonymous, check_prof_privilege, try_expect


@api_view(["GET"])
@check_anonymous
@try_expect(exceptions.NotFound, Course.DoesNotExist, Grade.DoesNotExist)
def course_grade_api(request, course_code):
    course = Course.objects.get(course_code=course_code)
    grade = Grade.objects.get(student=request.user, course=course)
    serialized = GradeSerializer(grade)
    grades = {
        "Final": grade.final,
        "Quizzes": grade.get_quiz_grades(),
        "Assignment": grade.get_assignment_grades(),
        "Midterm": grade.get_midterm_grades(),
        "Others": grade.other,
    }
    data = {"grade_data": serialized.data, "labels": grades.keys(), "data": grades.values(),"Total": grade.get_total_grades(), "course": course.course_code}
    return Response(data=data)


@api_view(["GET"])
@check_anonymous
@try_expect(exceptions.NotFound, Course.DoesNotExist, Quiz.DoesNotExist)
def course_quizzes_grade_api(request, course_code):
    course = Course.objects.get(course_code=course_code)
    quizzes = Quiz.objects.get_answered_quizzes(course=course, student=request.user)
    grades = {quiz.name: Quiz.objects.get_student_grade(quiz, request.user) for quiz in quizzes}
    data = {
        "labels": grades.keys(),
        "data": grades.values(),
    }
    return Response(data=data)


@api_view(["GET"])
@check_anonymous
@try_expect(exceptions.NotFound, Course.DoesNotExist, AssignmentGrade.DoesNotExist)
def course_assignments_grade_api(request,course_code):
    course = Course.objects.get(course_code=course_code)
    assignments_grades = AssignmentGrade.objects.filter(course=course,student=request.user).all()
    grades = {assign.assignment.name:assign.mark for assign in assignments_grades}
    data = {
        'labels':grades.keys(),
        'data':grades.values()
    }
    return Response(data=data)


@api_view(["GET"])
@check_anonymous
@try_expect(exceptions.NotFound, Course.DoesNotExist, Year.DoesNotExist, Semester.DoesNotExist, SemesterGrade.DoesNotExist)
def semester_course_grade_api(request, year, semester):
    year = Year.objects.get(year=year)
    semester = Semester.objects.get(semester=semester, year=year)
    grade = SemesterGrade.objects.get(student=request.user, year=year, semester=semester)
    serialized = SemesterGradeSerializer(grade)
    grades, total = grade.calc_total()
    labels = [course.course.name for course in grades.keys()]
    data = {"semester_grade": serialized.data, "labels": labels, "data": grades.values(), "total": total}
    return Response(data=data)


@api_view(["GET"])
@check_anonymous
@try_expect(exceptions.NotFound, Year.DoesNotExist, Course.DoesNotExist, MidtermGrade.DoesNotExist)
def midterm_grade_api(request, course_code, year):
    course=Course.objects.get(course_code=course_code)
    year = Year.objects.get(year=year)
    midterm = MidtermGrade.objects.filter(year=year, course=course, student=request.user).all()
    serialized = MidtermGradeSerializer(midterm)
    grades = {mid.semester.semester: mid.mark for mid in midterm}
    data = {
        "midterm": serialized.data,
        "labels": grades.keys(),
        "data": grades.values(),
        "avg": sum(grades.values()) / midterm.count(),
    }
    return Response(data=data)


@api_view(["GET"])
@check_anonymous
@try_expect(exceptions.NotFound, Year.DoesNotExist, MidtermGrade.DoesNotExist)
def year_midterm_api(request, year):
    year = Year.objects.get(year=year)
    midterm_grades = MidtermGrade.objects.filter(year=year, student=request.user).all()
    serializer = MidtermGradeSerializer(instance=midterm_grades, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@check_anonymous
@try_expect(exceptions.NotFound, Course.DoesNotExist)
def course_data_api(request, code):
    course = Course.objects.get(course_code=code)
    serialized = CourseSerializer(course, context={"request": request})
    return Response(serialized.data)


@api_view(["GET"])
@check_anonymous
@try_expect(exceptions.NotFound, QuizGrade.DoesNotExist, Quiz.DoesNotExist)
def quiz_grade_api(request, quiz_slug):
    quiz = Quiz.objects.get(slug=quiz_slug)
    quiz_grade = QuizGrade.objects.get(quiz=quiz, student=request.user)
    serialized = QuizGradeSerializer(quiz_grade)
    return Response(serialized.data)


@api_view(["GET"])
@check_anonymous
@try_expect(exceptions.NotFound, Assignment.DoesNotExist, AssignmentGrade.DoesNotExist)
def assignment_grade_api(request, slug):
    assignment = Assignment.objects.get(slug=slug)
    assignment_grade = AssignmentGrade.objects.get(assignment=assignment, student=request.user)
    serialized = AssignmentGradeSerializer(assignment_grade)
    return Response(serialized.data)


@api_view(["GET"])
@check_anonymous
@try_expect(exceptions.NotFound, Quiz.DoesNotExist)
def quiz_data_api(request, slug):
    quiz = Quiz.objects.get(slug=slug)
    serialized = QuizSerializer(quiz)
    return Response(serialized.data)


@api_view(["GET"])
@check_anonymous
@try_expect(exceptions.NotFound, Announcement.DoesNotExist)
def announcement_detail_api(request, slug):
    announcement = Announcement.objects.get(slug=slug)
    serialized = AnnouncementSerializer(announcement)
    return Response(serialized.data)


@api_view(["GET"])
@check_anonymous
@try_expect(exceptions.NotFound, Assignment.DoesNotExist)
def assignment_detail_api(request, slug):
    assignment = Assignment.objects.get(slug=slug)
    serialized = AssignmentSerializer(assignment)
    return Response(serialized.data)


@api_view(["GET"])
@check_anonymous
@check_prof_privilege
@try_expect(exceptions.NotFound, QuizGrade.DoesNotExist)
def quiz_grades_detail_api(request, slug):
    avg, count, name, total = QuizGrade.objects.get_quiz_avg(slug)
    data = {"name": name, "total": total, "avg": avg, "count": count}
    return Response(data=data)


@api_view(["GET"])
@check_anonymous
@check_prof_privilege
@try_expect(exceptions.NotFound, QuizGrade.DoesNotExist)
def quiz_grade_search_api(request, slug, mark, type):
    if type.lower() == "greater":
        grades = QuizGrade.objects.get_grades_passes(slug, mark)
    elif type.lower() == "lower":
        grades = QuizGrade.objects.get_grades_under(slug, mark)
    else:
        raise exceptions.NotAcceptable(detail="Check Your type")
    serialized = QuizGradeSerializer(grades, many=True)
    return Response(serialized.data)


@api_view(["GET"])
@check_anonymous
@check_prof_privilege
@try_expect(exceptions.NotFound, QuizGrade.DoesNotExist)
def course_quizzes_detail(request, course_code, year):
    avg = QuizGrade.objects.get_course_avg(course_code, year)
    return Response(data={"avg": avg})


@api_view(["GET"])
@check_anonymous
@check_prof_privilege
@try_expect(exceptions.NotFound, MidtermGrade.DoesNotExist)
def midterm_grade_search_api(request, course_code, semester, year, mark, type):
    if type.lower() == "greater":
        grades = MidtermGrade.objects.get_grades_gt(course_code, semester, year, mark)
    elif type.lower() == "lower":
        grades = MidtermGrade.objects.get_grades_lt(course_code, semester, year, mark)
    else:
        raise exceptions.NotAcceptable(detail="Check Your type")
    data = MidtermGradeSerializer(grades, many=True)
    return Response(data.data)


@api_view(["GET"])
@check_anonymous
@check_prof_privilege
@try_expect(exceptions.NotFound, SemesterGrade.DoesNotExist)
def student_semester_grade_api(request, college_id, semester, year):
    return Response(SemesterGrade.objects.get_student_semester_grades(college_id, semester, year))


@api_view(["GET"])
@check_anonymous
@check_prof_privilege
@try_expect(exceptions.NotFound, SemesterGrade.DoesNotExist)
def students_semester_grade_detail_api(request, semester, year):
    return Response(SemesterGrade.objects.get_semester_grades_avg(semester, year))


@api_view(["GET"])
@check_anonymous
@check_prof_privilege
@try_expect(exceptions.NotFound, Grade.DoesNotExist)
def grades_search_api(request, course_code, grade, year, type):
    if type.lower() == "greater":
        results, count = Grade.objects.get_passed_grade(course_code, grade, year)
    elif type.lower() == "lower":
        results, count = Grade.objects.get_un_passed_grade(course_code, grade, year)
    else:
        raise exceptions.NotAcceptable(detail="Check Your type")
    data = {"count": count, "grades": GradeSerializer(results, many=True).data}
    return Response(data)


@api_view(["GET"])
@check_anonymous
@check_prof_privilege
@try_expect(exceptions.NotFound, Grade.DoesNotExist)
def course_grades_detail_api(request, course, year):
    avg, count, total = Grade.objects.get_avg_course_grades(course, year)
    data = {"total": total, "count": count, "avg": avg}
    return Response(data)


@api_view(["GET"])
@check_anonymous
@try_expect(exceptions.NotFound, Grade.DoesNotExist)
def get_student_grades(request, student_id, year):
    data = GradeSerializer(Grade.objects.get_student_grades(student_id, year), many=True)
    return Response(data.data)


@api_view(["GET"])
@check_anonymous
@try_expect(exceptions.NotFound, Quiz.DoesNotExist)
def check_quiz_time_api(request, slug):
    quiz = Quiz.objects.get(slug=slug)
    return Response(data=quiz.is_open)


@api_view(["GET"])
@check_anonymous
@try_expect(exceptions.NotFound, Course.DoesNotExist, Questions.DoesNotExist)
def course_questions(request, course_code):
    course = Course.objects.get(course_code=course_code)
    questions = Questions.objects.filter(course=course).all()
    data = QuestionsSerializer(questions, many=True)
    count = questions.count()
    return Response(data={"data": data.data, "count": count})


@api_view(["GET"])
@check_anonymous
@try_expect(exceptions.NotFound, Questions.DoesNotExist)
def student_questions(request):
    questions = Questions.objects.filter(author=request.user).all()
    data = QuestionsSerializer(questions, many=True)
    count = questions.count()
    return Response(data={"data": data.data, "count": count})


@api_view(["PUT"])
@check_anonymous
@try_expect(exceptions.NotFound, Questions.DoesNotExist)
def update_question(request, slug):
    question = Questions.objects.get(slug=slug)
    question.edited = True
    serializer = QuestionsSerializer(question, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@check_anonymous
@try_expect(exceptions.NotFound, Answers.DoesNotExist)
def get_answers(request):
    answers = Answers.objects.filter(author=request.user).all()
    count = answers.count()
    data = {"data": AnswersSerializer(answers, many=True).data, "count": count}
    return Response(data=data)


@api_view(["POST"])
@check_anonymous
@try_expect(exceptions.NotFound, Questions.DoesNotExist)
def create_answer(request, question_slug):
    question = Questions.objects.get(slug=question_slug)
    answer = Answers(author=request.user, question=question, body=request.data.get("body"))
    serializer = AnswersSerializer(answer)
    answer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["PUT"])
@check_anonymous
@try_expect(exceptions.NotFound, Answers.DoesNotExist)
def update_answer(request, slug):
    answer = Answers.objects.get(slug=slug)
    answer.edited = True
    answer.body = request.data.get("body")
    serializer = AnswersSerializer(answer)
    answer.save()
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
