from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils.text import slugify


class Course(models.Model):
    name = models.CharField(_('Course Name'), max_length=100, unique=True)
    slug = models.SlugField(_('Course Slug'), max_length=255, unique=True, default='', editable=False)
    students = models.ManyToManyField(get_user_model(), related_name='courses_taken', through='Enrolment')
    instructor = models.ForeignKey(get_user_model(), related_name='courses_instructed', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        db_table = "course"
        verbose_name = _("Course")
        verbose_name_plural = _("Courses") # Translate to multiple languages if necessary

    def __str__(self):
        return self.name


class Enrolment(models.Model):
    # Pivot table: links courses and students through m:n relationship
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    course = models.ForeignKey('attendance.Course', related_name='enrolments', on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(_('Date Enrolled'), auto_now_add=True)

    class Meta:
        db_table = "enrolment"
        verbose_name = _("Enrolment")
        verbose_name_plural = _("Enrolment")
        unique_together = ('student', 'course',)

    def __str__(self):
        return f'{self.course} Enrolment'


class Attendance(models.Model):
    course = models.ForeignKey('attendance.Course', on_delete=models.CASCADE, related_name='attendance')
    students = models.ManyToManyField(get_user_model(), through='Proof')
    total_enrolment =  models.IntegerField()
    timestamp = models.DateTimeField(_('Lesson Time'), auto_now_add=True)

    class Meta:
        db_table = "attendance"
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendance")

    def __str__(self):
        return self.timestamp


class Proof(models.Model):
    # Pivot table: links attendnce and students through m:n relationship
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    attendance = models.ForeignKey('attendance.Attendance', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(_('Date Clocked'), auto_now_add=True)
    proof_pic = models.ImageField(null=True, blank=True)

    class Meta:
        db_table = "attendance_proof"
        verbose_name = _("Attendance Proof")
        verbose_name_plural = _("Attendance Proof")
        unique_together = ('student', 'attendance',)

    def __str__(self):
        return f'{self.attendance} Proof'
