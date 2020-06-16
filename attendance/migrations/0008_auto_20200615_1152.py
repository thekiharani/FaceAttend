# Generated by Django 3.0.7 on 2020-06-15 11:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0007_auto_20200615_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='lesson_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Lesson Date'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lesson',
            name='lesson_time',
            field=models.TimeField(verbose_name='Lesson Time'),
        ),
    ]
