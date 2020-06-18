import os
import secrets

from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    name = models.CharField(_('Full Name'), max_length=255)
    email = models.EmailField(_('Email Address'), unique=True)
    face_pic = models.ImageField(
        _('Choose Profile Picture'), null=True, blank=True,
        help_text='''For students, please upload a photo showing your face.
        This will be used to record your attendance through facial recognition.'''
    )
    is_instructor = models.BooleanField(
        _('I am a Course Instructor'), default=False,
        help_text='''Please check this field only if you are a course instructor.
        For students, please leave this unchecked.'''
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.face_pic:
            img = Image.open(self.face_pic.path)
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(self.face_pic.path)
            picture_fn = random_hex + f_ext
            picture_path = os.path.join(settings.BASE_DIR, 'media', picture_fn)

            if img.height > 400 or img.width > 400:
                output_size = (400, 400)
                img.thumbnail(output_size)
                os.remove(self.face_pic.path)
                self.face_pic = picture_fn
                img.save(picture_path)
                self.save()

    def __str__(self):
        return self.name
