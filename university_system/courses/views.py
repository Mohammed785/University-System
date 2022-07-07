from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import FileResponse, HttpResponseForbidden
from .models import Course, Announcement, Assignment, CourseFiles, Questions, Answers
from .forms import AnnouncementForm, AssignmentForm, CourseFilesForm, QuestionForm
from users.decorators import check_prof_privilege
from users.utils import delete_check

@login_required
def courses_list(request):
    courses = Course.objects.filter(students__id=request.user.id).all()
    return render(request, "course/courses.html", context={"courses": courses})


@login_required
def course_view(request, course_code):
    course = get_object_or_404(Course, course_code=course_code)
    return render(request, "course/course_view.html", context={"course": course})


@login_required
def course_assignments(request, course_code):
    course = get_object_or_404(Course, course_code=course_code)
    if not course.check_user_enrollment(request.user):
        messages.warning(request, "You Are Not Enrolled in This Course")
        return redirect("home")
    assignments_list = Assignment.objects.filter(course=course).order_by("upload_date").all()
    page = request.GET.get("page", 1)
    paginator = Paginator(assignments_list, 10)
    try:
        assignments = paginator.page(page)
    except PageNotAnInteger:
        assignments = paginator.page(1)
    except EmptyPage:
        assignments = paginator.page(paginator.num_pages)
    form = AssignmentForm()
    if request.method == "POST":
        if not request.user.is_prof:
            return HttpResponseForbidden()
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assign = form.save(commit=False)
            assign.course = course
            assign.professor = request.user
            assign.save()
            form.save()
            messages.success(request, "Assignment Added")
            return redirect("course-assignments", course_code=course.course_code)
    context = {"assignments": assignments, "course": course, "form": form}
    return render(request, "course/course_assignments.html", context=context)


@login_required
@check_prof_privilege
def assignment_update(request, slug):
    assignment = get_object_or_404(Assignment, slug=slug)
    form = AssignmentForm(instance=assignment)
    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment Updated")
            return redirect("course-assignments", course_code=assignment.course.course_code)
    context = {"assignment": assignment, "form": form}
    return render(request, "course/assignment_update.html", context=context)


@login_required
def course_announcements(request, course_code):
    course = get_object_or_404(Course, course_code=course_code)
    if not course.check_user_enrollment(request.user):
        messages.warning(request, "You Are Not Enrolled in This Course")
        return redirect("home")
    announcements_list = Announcement.objects.filter(course=course).all()
    page = request.GET.get("page", 1)
    paginator = Paginator(announcements_list, 10)
    try:
        announcements = paginator.page(page)
    except PageNotAnInteger:
        announcements = paginator.page(1)
    except EmptyPage:
        announcements = paginator.page(paginator.num_pages)
    form = AnnouncementForm()
    if request.method == "POST":
        if not request.user.is_prof:
            return HttpResponseForbidden()
        form = AnnouncementForm(request.POST)
        announcement = form.save(commit=False)
        announcement.author = request.user
        announcement.course = course
        announcement.save()
        form.save()
        messages.success(request, "Announcement Added")
        return redirect("course-announcements", course_code=course.course_code)
    context = {"course": course, "announcements": announcements, "form": form}
    return render(request, "course/course_announcements.html", context=context)


@login_required
@check_prof_privilege
def announcement_update(request, slug):
    announcement = get_object_or_404(Announcement, slug=slug)
    form = AnnouncementForm(instance=announcement)
    if request.method == "POST":
        form = AnnouncementForm(request.POST,instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, "Announcement Updated")
    context = {"announcement": announcement, "form": form}
    return render(request, "course/announcement_update.html", context=context)


@login_required
def course_files_view(request, course_code):
    course = get_object_or_404(Course, course_code=course_code)
    if not course.check_user_enrollment(request.user):
        messages.success(request, "Your Are Not Enrolled In This Course")
        return redirect("home")
    files = CourseFiles.objects.filter(course=course).all()
    form = CourseFilesForm()
    if request.method == "POST":
        if not request.user.is_prof:
            return HttpResponseForbidden()
        form = CourseFilesForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.course = course
            file.uploader = request.user
            file.save()
            form.save()
            return redirect("course-files", course_code=course.course_code)
    count = files.count()
    context = {"files": files, "count": count, "course": course, "form": form}
    return render(request, "course/course_files.html", context=context)


@login_required
@check_prof_privilege
def delete_assignment(request, slug):
    assignment = get_object_or_404(Assignment, slug=slug)
    if not delete_check(request,"You Are Not Allowed To Delete This Assignment",assignment.professor):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    assignment.delete()
    messages.success(request, "Assignment Deleted")
    return redirect("course-assignments", course_code=assignment.course.course_code)


@login_required
@check_prof_privilege
def delete_announcement(request, slug):
    announcement = get_object_or_404(Announcement, slug=slug)
    if not delete_check(request,"You Are Not Allowed To Delete This Announcement",announcement.author):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    announcement.delete()
    messages.success(request, "Announcement Deleted")
    return redirect("course-announcements", course_code=announcement.course.course_code)


@login_required
@check_prof_privilege
def delete_course_file(request, slug):
    file = get_object_or_404(CourseFiles, slug=slug)
    if not delete_check(request,"You Are Not Allowed To Delete This File",file.uploader):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    file.delete()
    messages.success(request, "File Deleted")
    return redirect("course-files", course_code=file.course.course_code)


@login_required
def course_questions(request, course_code):
    course = get_object_or_404(Course, course_code=course_code)
    questions_list = Questions.objects.filter(course=course).order_by("-date_posted").all()
    if not course.check_user_enrollment(request.user):
        messages.success(request, "Your Are Not Enrolled In This Course")
        return redirect("home")
    page = request.GET.get("page", 1)
    paginator = Paginator(questions_list, 10)
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    context = {"course": course, "questions": questions}
    return render(request, "course/course_questions.html", context=context)

@login_required
def question_update(request,slug):
    question = get_object_or_404(Questions,slug=slug)
    form = QuestionForm(instance=question)
    if request.method =='POST':
        form = QuestionForm(request.POST,instance=question)
        if form.is_valid():
            form.save()
            messages.success(request,'Question Updated')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    return render(request,'course/edit_question.html',context={'form':form,'question':question})

@login_required
def delete_question(request,slug):
    question = get_object_or_404(Questions,slug=slug)
    if not delete_check(request,'You Are Not Allowed To Delete This Question',question.author):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    question.delete()
    return redirect('course-questions',course_code=question.course.course_code)


@login_required
def delete_answer(request,slug):
    answer = get_object_or_404(Answers,slug=slug)
    if not delete_check(request,"You Are Not Allowed To Delete This Answer",answer.author):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    answer.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


@login_required
def download_file(request, filepath):
    return FileResponse(open(filepath, "rb"))
