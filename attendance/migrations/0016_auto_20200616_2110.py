# Generated by Django 3.0.7 on 2020-06-16 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0015_auto_20200616_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='attendance.Lesson'),
        ),
    ]
