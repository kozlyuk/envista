"""
Custom user model manager for accounts.
"""

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.apps import apps


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        model = apps.get_model(app_label='accounts', model_name='User')
        if model.objects.filter(email=self.normalize_email(email)).exists():
            raise ValueError(_("User with such email already exist"))

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_registered = True
        user.save(using=self._db)
        return user
