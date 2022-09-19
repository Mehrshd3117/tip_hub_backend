from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User, OtpCode
from django.core import validators
# Tool packages
from ckeditor.widgets import CKEditorWidget


# User customize
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone', 'email', 'first_name', 'last_name', 'bio')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError("Passwords don't match")
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="You can change password using <a href=\"../password/\">this form</a>"
    )

    class Meta:
        model = User
        fields = (
            'phone',
            'email',
            'first_name',
            'last_name',
            'image',
            'bio',
            'password',
            'is_active',
            'is_admin'
        )


# User registration and login
class UserRegisterForm(forms.Form):
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'email-input', 'placeholder': 'نام '}
    ))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'email-input', 'placeholder': 'نام خانوادگی '}
    ))
    email = forms.EmailField(max_length=200, widget=forms.EmailInput(
        attrs={'class': 'email-input', 'placeholder': 'پست الکترونیک'}
    ))
    phone = forms.CharField(max_length=11, widget=forms.TextInput(
        attrs={'class': 'email-input', 'placeholder': 'شماره تماس'}),validators=[validators.MaxValueValidator(11)]
    )
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'password-input', 'dir': 'ltr', 'placeholder': 'گذرواژه'}
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'password-input1', 'dir': 'ltr', 'placeholder': 'تایید گذرواژه'}
    ))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user:
            raise ValidationError(_('This email is already available'))
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = User.objects.filter(phone_number=phone)
        if user:
            raise ValidationError(_('This mobile number is already available'))
        # Removed the otp code
        OtpCode.objects.filter(phone_number=phone).delete()
        return phone


class UserLoginForm(AuthenticationForm):
    email = forms.EmailField(max_length=200, widget=forms.EmailInput(
        attrs={'class': 'email-input', 'placeholder': 'پست الکترونیک'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'password-input', 'placeholder': 'گذرواژه'}
    ))
    error_messages = {
        "کاربری با این مشخصات موجود نیست",
    }


class UserEditForm(forms.ModelForm):
    bio = forms.CharField(required=False, widget=CKEditorWidget(
        attrs={'class': 'email-input', 'placeholder': 'درباره من '}
    ))
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'email-input', 'placeholder': 'نام '}
    ))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'email-input', 'placeholder': 'نام خانوادگی '}
    ))
    phone = forms.CharField(required=False, max_length=11, widget=forms.TextInput(
        attrs={'class': 'email-input', 'placeholder': 'شماره تماس'}), validators=[validators.MaxValueValidator(11)]
    )
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(
        attrs={'class': 'email-input', 'placeholder': 'پست الکترونیک'}
    ))
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'bio', 'image')


# one time Password
class VerifyForm(forms.Form):
    code = forms.CharField(label='کد', widget=forms.NumberInput(
        attrs={'class': 'email-input', 'placeholder': 'لطفا کد تایید را وراد کنید '}
    ))
