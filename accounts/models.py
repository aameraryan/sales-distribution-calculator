from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    ACCOUNT_TYPE_CHOICES = (("AG", "Agent"), ("ST", "Staff"), ("AD", "Admin"))

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    account_type = models.CharField(max_length=2, choices=ACCOUNT_TYPE_CHOICES, default="NU")

    photo = models.ImageField(upload_to="accounts/users/photos/", blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    @property
    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def get_short_name(self):
        return "{} {}".format(self.first_name, self.last_name[0])

    @property
    def get_display_text(self):
        return self.get_full_name

    @property
    def get_avatar(self):
        if self.photo:
            return self.photo.url
        else:
            return "missing"
