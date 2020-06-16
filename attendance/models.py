from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils.text import slugify

class Course(models.Model):
    name = models.CharField(_('Course Name'), max_length=100, unique=True)
    slug = models.SlugField(_('Course Slug'), max_length=255, unique=True, default='', editable=False)
    students = models.ManyToManyField(get_user_model(), related_name='courses_taken', through='Enrolment')
    instructor = models.ForeignKey(get_user_model(), related_name='courses_instructed', on_delete=models.CASCADE)
    description = models.TextField(_('Course Description'), null=True, blank=True)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self):
        return self.name

class Enrolment(models.Model):
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    course = models.ForeignKey('attendance.Course', on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(_('Date Enrolled'), auto_now_add=True)
    final_grade = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        verbose_name = _("Enrolment")
        verbose_name_plural = _("Enrolment")
        unique_together = ('student', 'course',)

    def __str__(self):
        return f'{self.course} Enrolment'

class Lesson(models.Model):
    instructor = models.ForeignKey(get_user_model(), related_name='lessons', on_delete=models.CASCADE)
    course = models.ForeignKey('attendance.Course', on_delete=models.CASCADE)
    lesson_time = models.DateTimeField(_('Lesson Date'), auto_now_add=True)

    class Meta:
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")

    def __str__(self):
        return f'{self.course} Lesson'

class Attendance(models.Model):
    lesson = models.ForeignKey('attendance.Lesson', on_delete=models.CASCADE)
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    timestamp = models.DateTimeField(_('Lesson Time'), auto_now_add=True)

    class Meta:
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendance")
        unique_together = ('lesson', 'student',)

    def __str__(self):
        return self.timestamp
