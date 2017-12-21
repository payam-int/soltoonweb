from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'website/home.html'
    def get(self, request):
        return render(request, self.template_name)

class Login(LoginView):
    template_name = 'website/login.html'
    redirect_authenticated_user = True
    def get(self, request):
        return render(request, self.template_name)

class Game(TemplateView):
    template_name = 'website/game.html'
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)