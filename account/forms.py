from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import NewUser


# User customize
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = NewUser
        fields = ('username', 'phone_number', 'email', 'first_name', 'about')

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
        model = NewUser
        fields = (
            'phone_number',
            'email',
            'username',
            'fullname',
            'about',
            'password',
            'is_active',
            'is_admin'
        )


# User registration and login
class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'class': 'email-input', 'placeholder': 'نام کاربری'}
    ))
    fullname = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'class': 'email-input', 'placeholder': 'نام و نام خانوادگی'}
    ))
    email = forms.EmailField(max_length=200, widget=forms.EmailInput(
        attrs={'class': 'email-input', 'placeholder': 'پست الکترونیک'}
    ))
    phone_number = forms.CharField(max_length=11, widget=forms.TextInput(
        attrs={'class': 'email-input', 'placeholder': 'شماره تماس'}
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'password-input', 'placeholder': 'گذرواژه'}
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'password-input', 'placeholder': 'تایید گذرواژه'}
    ))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = NewUser.objects.filter(email=email)
        if user:
            raise ValidationError(_('This email is already available'))
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        user = NewUser.objects.filter(phone_number=phone_number)
        if user:
            raise ValidationError(_('This mobile number is already available'))
        return phone_number


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11, widget=forms.TextInput(
        attrs={'class': 'email-input', 'placeholder': 'شماره تماس'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'password-input', 'placeholder': 'گزرواژه'}
    ))
