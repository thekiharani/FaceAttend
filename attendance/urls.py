from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('courses/', views.CoursesList.as_view(), name='courses'),
    path('courses/add/', views.CourseCreate.as_view(), name='course_create'),
    path('my_courses/', views.EnrolmentList.as_view(), name='my_courses'),
    path('course/<int:pk>/drop/', views.EnrolmentDelete.as_view(), name='course_drop'),
    path('course/<int:pk>/delete/', views.CourseDelete.as_view(), name='course_delete'),
    path('register_course/', views.EnrolmentCreate.as_view(), name='register_course'),
    path('attendance/<int:pk>/', views.AttendanceList.as_view(), name='attendance'),
    path('live_attendance/<int:pk>/', views.AttendanceLive.as_view(), name='live_attendance'),
    path('manual_attendance/', views.AttendanceCreate.as_view(), name='manual_attendance'),
    path('attendance_detail/<int:pk>/', views.AttendanceDetail.as_view(), name='attendance_detail'),

    # Ajax
    path('view_attendance/<int:pk>/', views.view_attendance, name='view_attendance'),
    path('update_attendance/', views.update_attendance, name='update_attendance'),
    path('view_proof/<int:pks>/<int:pka>/', views.view_proof, name='view_proof'),

    # Streaming
    path('video_feed/', views.video_feed, name='video_feed'),
]
