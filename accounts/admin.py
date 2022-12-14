from django.contrib import admin
from django.forms import Textarea
from . import forms
from .models import User, OtpCode
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin

admin.site.site_header = 'مدیریت سایت'
admin.site.site_title = 'صفحه مدیریت'
admin.site.index_title = 'تیپ هاب'


class UserAdminConfig(UserAdmin):
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm
    search_fields = ('email', 'first_name', 'last_name',)
    list_filter = ('is_active', 'is_admin')
    ordering = ('-start_date',)
    list_display = ('email', 'first_name', 'last_name', 'is_active',
                    'show_image', 'is_admin', 'is_superuser', 'start_date')
    fieldsets = (
        (None, {"fields": ("email", "phone", "first_name", "last_name", "image",)}),
        (_("Personal"), {"fields": ("instagram", "github", "linkedin", "twitter", "bio",)}),
        (_("Permissions"), {"fields": ("is_active", "is_admin", "is_superuser", "start_date")},),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'phone', 'password1', 'password2')}),
        ('Personal', {'fields': ('first_name', 'last_name', 'image', 'bio',
                                 'instagram', 'github', 'linkedin', 'twitter')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_superuser')}),
    )
    formfield_overrides = {
        User.bio: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }


class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code', 'expiration_date')
    list_filter = ('phone', 'expiration_date')


admin.site.register(User, UserAdminConfig)
admin.site.register(OtpCode, OtpCodeAdmin)
