from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('courses/', views.CoursesListView.as_view(), name='courses'),
    path('courses/add/', views.CourseCreateView.as_view(), name='course_create'),
    path('lessons/', views.LessonsListView.as_view(), name='lessons'),
    path('lessons/add/', views.LessonCreateView.as_view(), name='lesson_create'),
    path('my_courses/', views.EnrolmentListView.as_view(), name='my_courses'),
    path('register_course/', views.EnrolmentCreateView.as_view(), name='register_course'),
    path('attendance/', views.AttendanceListView.as_view(), name='attendance'),
    path('live_attendance/<int:lesson_id>/', views.AttendanceLive.as_view(), name='live_attendance'),
    path('manual_attendance/<int:lesson_id>/', views.AttendanceCreate.as_view(), name='manual_attendance'),
    path('attendance_detail/<int:pk>/', views.AttendanceDetail.as_view(), name='attendance_detail'),

    # Ajax
    path('update_attendance/<int:lesson_id>/', views.update_attendance, name='update_attendance'),

    # Streaming
    path('video_feed/', views.video_feed, name='video_feed'),
]
