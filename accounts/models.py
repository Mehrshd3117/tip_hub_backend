from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import CustomAccountManager
from django.utils.html import format_html
from django.urls import reverse
from ckeditor.fields import RichTextField


class User(AbstractUser, PermissionsMixin):
    username = None
    phone = models.CharField(unique=True, max_length=11, verbose_name='شماره تماس', null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name='پست الکترونیک')
    first_name = models.CharField(max_length=100, verbose_name='نام',
                                  blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name='نام خانوادگی',
                                 blank=True, null=True)
    image = models.ImageField(upload_to='user/', null=True, blank=True, verbose_name='عکس')
    bio = RichTextField(_('بیوگرافی'), null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ عضویت')
    is_admin = models.BooleanField(default=False, verbose_name='مدیر')
    is_active = models.BooleanField(default=True, verbose_name='فعال,غیرغعال')
    instagram = models.URLField(blank=True, null=True, unique=True,
                                verbose_name='آیدی اینستاگرام')
    github = models.URLField(blank=True, null=True, unique=True,
                             verbose_name='آدرس گیت هاب')
    linkedin = models.URLField(blank=True, null=True, unique=True,
                               verbose_name='آدرس لینکدین')
    twitter = models.URLField(blank=True, null=True, unique=True,
                              verbose_name='آدرس توییتر')

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def show_image(self):
        if self.image:
            return format_html(f'<img src="{self.image.url}" width="60px" height="60px">')
        return format_html(f'<h3 style="color: red">no image</h3>')

    show_image.short_description = 'عکس'

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.pk})

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربرها')

    @property
    def is_staff(self):
        return self.is_admin


class OtpCode(models.Model):
    phone = models.CharField(max_length=11, verbose_name='شماره تماس')
    code = models.IntegerField(verbose_name='رمز')
    expiration_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ انقضا')

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = _('رمز یک بار مصرف')
        verbose_name_plural = _('رمزهای یک بار مصرف')
