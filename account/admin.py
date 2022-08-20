from django.contrib import admin
from django.forms import Textarea
from .forms import *
from .models import NewUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    form = UserCreationForm
    add_form = UserChangeForm
    search_fields = ('email', 'username', 'fullname',)
    list_filter = ('is_active', 'is_admin')
    ordering = ('-start_date',)
    list_display = ('email', 'username', 'fullname',
                    'is_active', 'is_admin', 'is_superuser')
    fieldsets = (
        (None, {"fields": ("email", "phone_number", "username", "fullname")}),
        (_("Personal"), {"fields": ("about",)}),
        (_("Permissions"), {"fields": ("is_active", "is_admin", "is_superuser",)},),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",),
                "fields": ("email", "phone_number", "username", "fullname", "password1", "password2", "about")},
         ),
    )
    formfield_overrides = {
        NewUser.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }


admin.site.register(NewUser, UserAdminConfig)
