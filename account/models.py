from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from .managers import CustomAccountManager


class NewUser(AbstractUser, PermissionsMixin):
    phone_number = models.IntegerField(unique=True)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    fullname = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to='user/', null=True, blank=True)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'fullname', 'email']

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin


