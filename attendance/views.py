from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import StreamingHttpResponse
from .camera import VideoCamera
from .models import Course, Enrolment, Attendance, Lesson


class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['classes'] = Post.objects.all()
        return context

    template_name = 'attendance/home.html'


# Courses
class CoursesListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    def test_func(self):
        return self.request.user.is_instructor

    model = Course
    context_object_name = 'courses'
    template_name = 'attendance/courses_list.html'

    def get_queryset(self):
        return self.request.user.courses_instructed.all()


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
class LessonsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    def test_func(self):
        return self.request.user.is_instructor

    model = Lesson
    context_object_name = 'lessons'
    template_name = 'attendance/lessons_list.html'

    def get_queryset(self):
        return self.request.user.lessons.all()


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


# Attendance
class AttendanceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    def test_func(self):
        return self.request.user.is_instructor

    model = Lesson
    context_object_name = 'lessons'
    template_name = 'attendance/attendance_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_lesson = Lesson.objects.all().first()
        context['current_lesson'] = current_lesson
        return context


class AttendanceDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    def test_func(self):
        return self.request.user.is_instructor

    model = Lesson

    def get_object(self, **kwargs):
        return Lesson.objects.get(pk=self.kwargs['pk'])

    context_object_name = 'current_lesson'
    template_name = 'attendance/attendance_view.html'


class AttendanceLive(LoginRequiredMixin, UserPassesTestMixin, ListView):
    def test_func(self):
        return self.request.user.is_instructor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_lesson = Lesson.objects.get(pk=self.kwargs['lesson_id'])
        self.request.session['lesson'] = current_lesson.id
        context['lesson'] = current_lesson
        return context

    template_name = 'attendance/live_attendance.html'

    model = Attendance
    login_url = 'login'


class AttendanceCreate(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    def test_func(self):
        return self.request.user.is_instructor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_lesson = Lesson.objects.get(pk=self.kwargs['lesson_id'])
        self.request.session['lesson'] = current_lesson.id
        return context

    template_name = 'attendance/manual_attendance.html'
    success_message = 'Course enrolment successful'
    fields = ('student',)

    model = Attendance
    login_url = 'login'
    success_url = reverse_lazy('attendance:attendance')

    def form_valid(self, form):
        form.instance.lesson_id = self.request.session['lesson']
        return super().form_valid(form)


def gen(camera, lesson):
    while True:
        frame = camera.get_frame(lesson)
        yield (b'...frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
    lesson = request.session['lesson']
    return StreamingHttpResponse(gen(VideoCamera(), lesson),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


# Ajax routes
from django.core.serializers import serialize
from django.http import JsonResponse


def update_attendance(request, lesson_id):
    attendees = Attendance.objects.filter(lesson_id=lesson_id)
    return JsonResponse(serialize('json', attendees, cls=LazyEncoder), safe=False)
