# django package
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views import View
from django.views.generic import UpdateView
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# my User and models
from .models import User, OtpCode
from video.models import Subscriber, Video
# my Forms
from .forms import *
# otp
from Code import send_otp_code
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
            OtpCode.objects.create(phone=cd['phone'], code=random_code)
            request.session['registration_info'] = {
                'email': cd['email'],
                'first_name': cd['first_name'],
                'last_name': cd['last_name'],
                'phone': cd['phone'],
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
        code_otp = OtpCode.objects.get(phone=user_session['phone'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == str(code_otp.code):
                user = User.objects.create_user(
                    first_name=user_session['first_name'],
                    last_name=user_session['last_name'],
                    email=user_session['email'],
                    phone=user_session['phone'],
                    password=user_session['password']
                )
                code_otp.delete()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, "You're registered.", 'success')
                return redirect('home:main')
            else:
                messages.error(request, "This code is wrong!", 'danger')
                return redirect('accounts:verify')
        return redirect('home:main')


class UserLoginView(views.LoginView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('home:main')


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('home:main')


# UserProfile
class UserProfileView(View):

    def get(self, request, pk):
        form = get_object_or_404(User, pk=pk)
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


class UserMastersView(View):
    template_name = 'accounts/masters.html'

    def get(self, request, *args, **kwargs):
        master = User.objects.all().filter(is_superuser=True, is_admin=True)

        context = {
            'form': master,
        }

        return render(request, self.template_name, context)


# favourite video

class User_Favourite_List(View):
    template_name = 'accounts/favourites.html'

    def get(self, request):
        video_list = Video.objects.all().filter(favourites=request.user)
        context = {
            'videos': video_list
        }
        return render(request, self.template_name, context)


class User_Favourite_Add(View):
    def get(self, request, myid):
        video = get_object_or_404(Video, id=myid)
        if video.favourites.filter(id=request.user.id).exists():
            video.favourites.remove(request.user)
        else:
            video.favourites.add(request.user)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


# Master information
def user_master_info(request, pk, *args, **kwargs):
    master_info = User.objects.get(is_superuser=True, is_admin=True, pk=pk)
    user_id = kwargs.get('user_id')
    all_subscriber = Subscriber.objects.get_or_create(user=User.objects.get(pk=user_id))[0]

    is_self = True
    user = request.user

    if user.is_authenticated and user != master_info:
        is_self = False
    subscribed = False
    if user in all_subscriber.subscribers.all():
        subscribed = True
    else:
        subscribed = False

    count_subscribe = all_subscriber.subscribers.all().count()
    subscribed = False

    context = {
        'master_info': master_info,
        'is_self': is_self,
        'subscribed': subscribed,
        'count_subscribe': count_subscribe
    }

    return render(request, 'accounts/master_information.html', context)


# Password change
class PasswordChange(views.PasswordChangeView):
    success_url = reverse_lazy("accounts:password_change_done")
    template_name = "accounts/password_reset/password_change.html"


class PasswordChangeDone(views.PasswordChangeDoneView):
    template_name = "accounts/password_reset/password_change_done.html"


#  Reset forgotten password
class UserPasswordReset(views.PasswordResetView):
    template_name = 'accounts/password_reset/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            form.add_error('email', 'کاربری با این ایمیل موجود نیست')
            return super(UserPasswordReset, self).form_invalid(form)
        else:
            return super(UserPasswordReset, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('account:login')
        return super().get(*args, **kwargs)


class UserPasswordResetDone(views.PasswordResetDoneView):
    template_name = 'accounts/password_reset/password_reset_done.html'


class UserPasswordResetConfirm(views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetComplete(views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset/password_reset_complete.html'
