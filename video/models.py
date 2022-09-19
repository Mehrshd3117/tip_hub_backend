from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
# jalali
from extensions.utils import jalali_converter
# comment
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
# my user
from accounts.models import User


class IpAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='ادرس آی پی')

    def __str__(self):
        return self.ip_address

    class Meta:
        verbose_name = _('آدرس ای پی ')
        verbose_name_plural = _('آدرس ای پی ها')


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('عنوان دسته بندی'))
    slug = models.SlugField(unique=True, null=True, blank=True, allow_unicode=True, verbose_name=_('ادرس اینترنت'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name="children", verbose_name=_('فرزند'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('زمان ساخت'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('زمان بروزرسانی'))

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug = slugify(self.title)
        super(Category, self).save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('دسته بندی')
        verbose_name_plural = _('دسته بندی ها')


class Video(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('سازنده ویدیو'))
    title = models.CharField(max_length=225, unique=True, verbose_name=_('عنوان ویدیو'))
    description = RichTextField(verbose_name=_('توضیحات فیلم'))
    video = models.FileField(upload_to='videos/', verbose_name=_(' ویدیو'))
    category = models.ManyToManyField(Category, verbose_name='زیر دسته', related_name='video_category',)
    image = models.ImageField(upload_to='videos/image/', verbose_name=_('عکس کاور فیلم'))
    views = models.ManyToManyField(IpAddress, through="VideoView", blank=True, verbose_name=_('بازدیدها'))
    time = models.IntegerField(default=1, verbose_name=_('زمان فیلم'))
    slug = models.SlugField(blank=True, unique=True, verbose_name=_('ادرس اینترنت'))
    comments = GenericRelation(Comment, verbose_name=_('نظرها'))
    favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ساخت'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('بروزرسانی'))
    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')


    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug = slugify(self.title)
        super(Video, self).save()

    def get_absolute_url(self):
        return reverse('videos:video_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def jalali_created(self):
        return jalali_converter(self.publish)
    jalali_created.short_description = 'زمان انتشار'

    class Meta:
        verbose_name = _('ویدیو')
        verbose_name_plural = _('ویدیو ها')


class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    subscribers = models.ManyToManyField(User, related_name='subscribers', verbose_name=_('اشتراک ها'))

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = _('اشتراک')
        verbose_name_plural = _('اشتراک ها')


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like', verbose_name=_('کاربر'))
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes', verbose_name=_('ویدیو'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.video.title}"

    class Meta:
        verbose_name = _("لایک")
        verbose_name_plural = _("لایک ها ")
        ordering = ("-created_at",)


class VideoView(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name=_('عنوان ویدیو'))
    ip_address = models.ForeignKey(IpAddress, on_delete=models.CASCADE, verbose_name=_('آدرس ای پی'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ساخت'))

    def __str__(self):
        return self.video.title

    class Meta:
        verbose_name = _(' بازدید ویدیو')
        verbose_name_plural = _(' بازدید ویدیو ها')
