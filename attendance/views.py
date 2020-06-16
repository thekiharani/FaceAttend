from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Course, Lesson, Enrolment

class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['classes'] = Post.objects.all()
        return context

    template_name = 'attendance/home.html'


# Courses
class CoursesListView(LoginRequiredMixin, ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'attendance/courses_list.html'

    def get_queryset(self):
        if self.request.user.is_instructor:
            return self.request.user.courses_instructed.all()
        else:
            return self.request.user.courses_taken.all()

class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    def test_func(self):
        return self.request.user.is_instructor

    success_message = 'Course successfully added'
    template_name = 'attendance/course_create.html'

    model = Course
    fields = ('name', 'description')
    success_url = reverse_lazy('attendance:courses')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super().form_valid(form)

# Lessons
class LessonsListView(LoginRequiredMixin, ListView):
    model = Lesson
    context_object_name = 'lessons'
    template_name = 'attendance/lessons_list.html'

    def get_queryset(self):
        if self.request.user.is_instructor:
            return Lesson.objects.filter(instructor=self.request.user)
        else:
            return Lesson.objects.all()

class LessonCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    def test_func(self):
        return self.request.user.is_instructor

    success_message = 'Lesson successfully added'
    template_name = 'attendance/lesson_create.html'

    model = Lesson
    fields = ('course',)
    success_url = reverse_lazy('attendance:lessons')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super().form_valid(form)

# Enrolment
class EnrolmentListView(LoginRequiredMixin, ListView):
    model = Enrolment
    context_object_name = 'enrolments'
    template_name = 'attendance/enrolments_list.html'

    def get_queryset(self):
        return Enrolment.objects.filter(student=self.request.user)

class EnrolmentCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    def test_func(self):
        return not self.request.user.is_instructor

    success_message = 'Course enrolment successful'
    template_name = 'attendance/enrolment_create.html'

    model = Enrolment
    fields = ('course',)
    success_url = reverse_lazy('attendance:my_courses')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super().form_valid(form)