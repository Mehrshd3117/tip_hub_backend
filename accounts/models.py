from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import CustomAccountManager
from django.utils.html import format_html
from ckeditor.fields import RichTextField


class User(AbstractUser, PermissionsMixin):
    username = None
    phone_number = models.CharField(unique=True, max_length=11, null=True, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, verbose_name='نام',
                                  blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name='نام خانوادگی',
                                 blank=True, null=True)
    image = models.ImageField(upload_to='user/', null=True, blank=True)
    about = RichTextField(_(
        'about'), null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربرها')

    def show_image(self):
        if self.image:
            return format_html(f'<img src="{self.image.url}" width="60px" height="60px">')
        return format_html(f'<h3 style="color: red">no image</h3>')
    show_image.short_description = 'image'

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.IntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number




