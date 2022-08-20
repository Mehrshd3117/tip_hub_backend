from django.shortcuts import render
from django.views import View


class Home(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home/index.html')
