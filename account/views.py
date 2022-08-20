from django.shortcuts import render, redirect
from django.views import View

from .models import NewUser
from .forms import UserRegisterForm, UserLoginForm


# Using classes to register and log in and out of users
class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'account/register.html'

    def get(self, request):
        form = self.form_class
        if request.user.is_authenticated:
            return redirect('home:main')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class
        if form.is_valid():
            cd = form.cleaned_data
            NewUser.objects.create_user(
                username=cd['username'],
                fullname=cd['fullname'],
                email=cd['email'],
                phone_number=cd['phone_number'],
                password=cd['password1']
            )
            return redirect('home:main')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


