from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    name = models.CharField(_('Full Name'), max_length=255)
    email = models.EmailField(_('Email Address'), unique=True)
    face_pic = models.ImageField(_('Choose Profile Picture'), null=True, blank=True)
    is_instructor = models.BooleanField(
        _('Is Instructor'), default=False,
        help_text='Designates whether the user is an instructor'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    objects = CustomUserManager()

    def __str__(self):
        return self.name