# Generated by Django 3.0.7 on 2020-06-17 10:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendance', '0017_auto_20200616_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to='attendance.Course'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together=set(),
        ),
        migrations.CreateModel(
            name='Proof',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Date Clocked')),
                ('proof_pic', models.ImageField(blank=True, null=True, upload_to='')),
                ('attendance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.Attendance')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Attendance Proof',
                'verbose_name_plural': 'Attendance Proof',
                'unique_together': {('student', 'attendance')},
            },
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='lesson',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='proof',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='student',
        ),
        migrations.AddField(
            model_name='attendance',
            name='students',
            field=models.ManyToManyField(related_name='course_attendance', through='attendance.Proof', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Lesson',
        ),
    ]