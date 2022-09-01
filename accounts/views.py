# django package
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import UpdateView
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# my User and models
from .models import User, OtpCode
# my Forms
from .forms import *
# otp
from Token import send_otp_code
from random import randint
# Password reset and change
from django.contrib.auth import views


# Using classes to register and log in and out of users
class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        if request.user.is_authenticated:
            return redirect('home:main')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_code = randint(1000, 9999)
            send_otp_code(cd['phone_number'], random_code)
            OtpCode.objects.create(phone_number=cd['phone_number'], code=random_code)
            request.session['registration_info'] = {
                'email': cd['email'],
                'first_name': cd['first_name'],
                'last_name': cd['last_name'],
                'phone_number': cd['phone_number'],
                'password': cd['password1']
            }
            messages.success(request, 'We send you a code', 'success')
            return redirect('accounts:verify')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


# one time password
class VerifyCode(View):
    form_class = VerifyForm

    def get(self, request):
        form = self.form_class
        if request.user.is_authenticated:
            return redirect('home:main')
        return render(request, 'accounts/one-time-password.html', {'form': form})

    def post(self, request):
        user_session = request.session['registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            print('parimah')
            cd = form.cleaned_data
            if cd['code'] == str(code_instance.code):
                print('mehrshad')
                user = User.objects.create_user(
                    user_session['first_name'],
                    user_session['last_name'],
                    user_session['phone_number'],
                    user_session['email'],
                    user_session['password']
                )
                code_instance.delete()
                login(request, user)
                messages.success(request, "You're registered.", 'success')
                return redirect('home:main')
            else:
                messages.error(request, "This code is wrong!", 'danger')
                return redirect('accounts:verify')
        return redirect('home:main')


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class
        if request.user.is_authenticated:
            return redirect('home:main')

        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                return redirect('home:main')
            messages.error(request, "You're email or password is wrong", 'danger')

        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('home:main')


# UserProfile
class UserProfileView(View):

    def get(self, request, pk):
        form = get_object_or_404(User, id=pk)
        context = {
            'form': form,
        }
        return render(request, 'accounts/user-panel.html', context)


class UserEditProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserEditForm
    model = User
    template_name = 'accounts/edit-user-panel.html'

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)


# Password change
class PasswordChange(views.PasswordChangeView):
    success_url = reverse_lazy("accounts:password_change_done")
    template_name = "accounts/password_change.html"


class PasswordChangeDone(views.PasswordChangeDoneView):
    template_name = "accounts/password_change_done.html"


#  Reset forgotten password
class UserPasswordReset(views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'


class USerPasswordResetDone(views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class UserPasswordResetConfirm(views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetComplete(views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'



