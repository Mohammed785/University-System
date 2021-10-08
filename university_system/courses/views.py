from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import FileResponse,HttpResponseNotFound
from .models import Course, Announcement, Assignment, CourseFiles
from .forms import CreateAnnouncementForm, CreateAssignmentForm, CreateCourseFiles
from users.decorators import check_prof_previlage
from quizzes.models import Quiz



@login_required
def course_view(request, slug):
    course = get_object_or_404(Course, slug=slug)
    return render(request, "course/view.html", context={"course": course})


#check statues spelling
@login_required
def quiz_statues(request,slug,statues):
    course = get_object_or_404(Course, slug=slug)
    statues = statues.lower()
    if statues == 'open':
        quizzes = Quiz.objects.get_opened_quizzes(course)
        type_ = 'Open'
    elif statues == 'closed':
        quizzes = Quiz.objects.get_closed_quizzes(course)
        type_ = 'Closed'
    elif statues == 'answered':
        quizzes = Quiz.objects.get_answered_quizzes(course)
        type_ = 'Answered'
    elif statues == 'unanswered':
        quizzes = Quiz.objects.get_unanswered_quizzes(course)
        type_ = 'UnAnswered'
    else:
        return HttpResponseNotFound()
    context = {
        'course':course,
        'quizzes':quizzes,
        'type':type_
    }
    return render(request,'quiz/quiz_type.html',context=context)


@check_prof_previlage
@login_required
def create_assignment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if not course.check_user_enrollment(request.user):return redirect()
    form = CreateAssignmentForm()
    if request.method == "POST":
        form = CreateAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assign = form.save(commit=False)
            assign.course = course
            assign.professor = request.user
            assign.save()
            form.save()
            return redirect(assign.get_absolute_url())
    context = {"course": course, "form": form}
    return render(request, "course/create_assignment.html", context=context)


class ViewCourseAssignment(LoginRequiredMixin,UserPassesTestMixin, ListView):
    model = Course
    template_name = "course/course_assignments.html"
    context_object_name = "assignments"
    paginate_by = 5

    def test_func(self):
        course = self.get_object()
        if not course.check_user_enrollment(self.request.user):
            return False
        return True

    def get_object(self):
        return get_object_or_404(Course,slug=self.kwargs['slug'])

    def get_queryset(self):
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        return course.assignment_set.all()

class ViewAssignment(LoginRequiredMixin,DetailView):
    model = Assignment
    template_name = 'course/assignment_view.html'
    constext_object_name = 'assignment'
    

class UpdateAssignmentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Assignment
    fields = ["file", "deadline"]

    def test_func(self):
        if not self.request.user.is_prof:
            return False
        return True


class DeleteAssignmentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Assignment

    def test_func(self):
        if not self.request.user.is_prof:
            return False
        return True

    def get_success_url(self):
        course = self.get_object().course
        return redirect('course-assignments',slug=course.slug)


@check_prof_previlage
@login_required
def create_announcement(request, slug):
    course = get_object_or_404(Course, slug=slug)
    form = CreateAnnouncementForm()
    if request.method == "POST":
        form = CreateAnnouncementForm(request.POST)
        announcement = form.save(commit=False)
        announcement.author = request.user
        announcement.course = course
        announcement.save()
        form.save()
        return redirect(announcement.get_absolute_url())
    context = {"course": course, "form": form}
    return render(request, "course/announcement_create.html", context=context)


class AnnouncementView(LoginRequiredMixin,UserPassesTestMixin, DetailView):
    model = Announcement
    template_name = "course/announcement_view.html"
    context_object_name = "announcement"
    
    def test_func(self):
        course = self.get_object().course
        if not course.check_user_enrollment(self.request.user):
            return False
        return True


class ViewCourseAnnouncement(LoginRequiredMixin,UserPassesTestMixin, ListView):
    model = Course
    template_name = "course/course_announcements.html"
    context_object_name = "announcements"
    paginate_by = 5

    def test_func(self):
        course = self.get_object()
        if not course.check_user_enrollment(self.request.user):
            return False
        return True

    def get_queryset(self):
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        return course.announcement_set.all()


class UpdateAnnouncementView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Announcement
    fields = ["body"]

    def test_func(self):
        if not self.request.user.is_prof:
            return False
        return True


class DeleteAnnouncementView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Announcement

    def test_func(self):
        if not self.request.user.is_prof:
            return False
        return True

    def get_success_url(self):
        course = self.get_object().course
        return redirect('course-announcements',slug=course.slug)


@check_prof_previlage
@login_required
def add_course_file(request, slug):
    course = get_object_or_404(Course, slug=slug)
    form = CreateCourseFiles()
    if request.method == "POST":
        form = CreateCourseFiles(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.course = course
            file.uploader = request.user
            file.save()
            form.save()
            return redirect(file.get_absolute_url())
    context = {"course": course, "form": form}
    return render(request, "course/create_assignment.html", context=context)


class CourseFilesView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Course

    def test_func(self):
        course = self.get_object()
        if not course.check_user_enrollment(self.request.user):
            return False
        return True

    def get_queryset(self):
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        return course.coursefile_set.all()


class DeleteCourseFileView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CourseFiles

    def test_func(self):
        file = self.get_object()
        if self.request.user != file.uploader:
            return False
        return True

    def get_success_url(self):
        course = self.get_object().course
        return redirect('course-files-view',slug=course.slug)


@login_required
def download_file(request, filepath):
    return FileResponse(open(filepath, "rb"))
