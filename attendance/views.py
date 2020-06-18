from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import StreamingHttpResponse
from .camera import VideoCamera
from .models import Course, Enrolment, Attendance, Proof


class HomePage(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['classes'] = Post.objects.all()
        return context

    template_name = 'attendance/home.html'


# Courses
class CoursesList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    def test_func(self):
        return self.request.user.is_instructor

    model = Course
    context_object_name = 'courses'
    template_name = 'attendance/courses_list.html'

    def get_queryset(self):
        return self.request.user.courses_instructed.all()


class CourseCreate(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    def test_func(self):
        return self.request.user.is_instructor

    success_message = 'Course successfully added'
    template_name = 'attendance/course_create.html'

    model = Course
    fields = ('name',)
    success_url = reverse_lazy('attendance:courses')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super().form_valid(form)


class CourseDelete(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    def test_func(self):
        return self.request.user.is_instructor

    model = Course
    success_message = 'Course successfully deleted'
    template_name = 'attendance/course_delete.html'
    success_url = reverse_lazy('attendance:courses')


# Enrolment
class EnrolmentList(LoginRequiredMixin, ListView):
    model = Enrolment
    context_object_name = 'enrolments'
    template_name = 'attendance/enrolments_list.html'

    def get_queryset(self):
        return Enrolment.objects.filter(student=self.request.user)


class EnrolmentCreate(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
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


class EnrolmentDelete(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    def test_func(self):
        return not self.request.user.is_instructor

    model = Enrolment
    success_message = 'Course successfully dropped'
    template_name = 'attendance/course_drop.html'
    success_url = reverse_lazy('attendance:my_courses')


# Attendance
class AttendanceList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    def test_func(self):
        return self.request.user.is_instructor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(pk=self.kwargs['pk'])
        attendance = course.attendance.first()
        context['course'] = course
        context['attendance'] = attendance
        return context

    model = Attendance
    context_object_name = 'attendance_list'
    template_name = 'attendance/attendance_list.html'


class AttendanceLive(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    def test_func(self):
        return self.request.user.is_instructor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(pk=self.kwargs['pk'])
        attendance = Attendance.objects.create(course=course, total_enrolment=course.students.count())
        self.request.session['attendance_id'] = attendance.pk
        self.request.session['course_id'] = course.pk
        context['attendance'] = attendance
        return context

    context_object_name = 'course'
    template_name = 'attendance/live_attendance.html'

    model = Course
    login_url = 'login'


class AttendanceCreate(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    def test_func(self):
        return self.request.user.is_instructor

    template_name = 'attendance/manual_attendance.html'
    success_message = 'Course enrolment successful'
    fields = ('student',)

    model = Proof
    login_url = 'login'
    success_url = reverse_lazy('attendance:courses')

    def form_valid(self, form):
        form.instance.attendance_id = self.request.session['attendance_id']
        return super().form_valid(form)


def gen(camera, attendance_id, course_id):
    while True:
        frame = camera.get_frame(attendance_id, course_id)
        yield (b'...frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
    attendance_id = request.session['attendance_id']
    course_id = request.session['course_id']
    return StreamingHttpResponse(gen(VideoCamera(), attendance_id, course_id),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


# Ajax routes
def update_attendance(request):
    attendance = Attendance.objects.get(pk=request.session['attendance_id'])
    return render(request, 'attendance/ajax/update_attendance.html', {
        'attendance': attendance
    })


def view_attendance(request, pk=None):
    attendance = Attendance.objects.get(pk=pk)
    return render(request, 'attendance/ajax/attendance.html', {
        'attendance': attendance
    })


def view_proof(request, pks=None, pka=None):
    proof = Proof.objects.get(student_id=pks, attendance_id=pka)
    return render(request, 'attendance/ajax/proof.html', {
        'proof': proof
    })
