from django.urls import path
from .views import (
    HomeView, CoursesListView, CourseCreateView, LessonsListView, LessonCreateView, EnrolmentListView, EnrolmentCreateView
)

app_name = 'attendance'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('courses/', CoursesListView.as_view(), name='courses'),
    path('courses/add/', CourseCreateView.as_view(), name='course_create'),
    path('lessons/', LessonsListView.as_view(), name='lessons'),
    path('lessons/add/', LessonCreateView.as_view(), name='lesson_create'),
    path('my_courses/', EnrolmentListView.as_view(), name='my_courses'),
    path('register_course/', EnrolmentCreateView.as_view(), name='register_course'),
]
