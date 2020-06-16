from django.contrib import admin
from .models import Course, Enrolment, Lesson, Attendance

admin.site.register((Course, Enrolment, Lesson, Attendance))
