from django.contrib import admin
from .models import Course, Enrolment, Proof, Attendance

admin.site.register((Course, Enrolment, Proof, Attendance))
