# Generated by Django 3.0.7 on 2020-06-18 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0019_auto_20200618_1848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='description',
        ),
    ]
