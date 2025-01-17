# Generated by Django 3.0.7 on 2020-06-16 10:19

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendance', '0012_auto_20200616_0955'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('lesson', 'student')},
        ),
        migrations.AlterUniqueTogether(
            name='enrolment',
            unique_together={('student', 'course')},
        ),
    ]
