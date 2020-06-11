from django.contrib import admin
from .models import Course, Enrollement, Lesson, Attendance

admin.site.register((Course, Enrollement, Lesson, Attendance))
