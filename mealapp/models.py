from django.db import models
from django.contrib. auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone


class AuthUser(AbstractBaseUser, PermissionsMixin):
    """
    Simple custom user model
    """
    # Basic fields
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)

    # Status fields
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # Timestamp
    date_joined = models.DateTimeField(default=timezone.now)

    # Required for Django admin (we'll use it later)
    is_staff = models.BooleanField(default=False)

    # This tells Django which field to use for login
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
