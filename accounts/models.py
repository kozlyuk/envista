""" Models for managing accounts """

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from accounts.managers import CustomUserManager


class User(AbstractUser):
    """
    Custom user model where email is the unique identifiers
    for authentication instead of usernames.
    Added fields mobile_number, birth_date, avatar, theme
    """
    #  Fields
    username = None
    email = models.EmailField(_('Email address'), unique=True)
    mobile_number = models.CharField(_('Mobile number'), max_length=10, blank=True)
    address = models.CharField(_('Address'), max_length=255, blank=True)
    comment = models.CharField(_('Comment'), max_length=255, blank=True)
    telegram_id = models.PositiveIntegerField(blank=True, null=True)
    is_registered = models.BooleanField(_('Registered'), default=False,
        help_text=_('Designates whether this user aprooved by administrator.'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name
