from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, FormView
from formtools.wizard.views import SessionWizardView
from requests import post

from sandbox.models import Code
from website.forms import UserInformationForm, SoltoonForm, UploadCodeForm


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

    def get_context_data(self, **kwargs):
        context = super(Game, self).get_context_data(**kwargs)

        context['user'] = self.request.user
        context['upload_code'] = {
            'form': UploadCodeForm,
            'action': reverse('soltoonwebsite_uploadcode')
        }

        context['codes'] = Code.objects.filter(user=self.request.user).order_by('-created_at')[:10]

        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        request_user = request.user
        if not (request_user.information.exists()) or not (request_user.soltoon.exists()):
            return HttpResponseRedirect(reverse('soltoonwebsite_registergame'))

        return super(Game, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, 'dispatch')
class RegisterGame(SessionWizardView):
    form_list = [('soltoon', SoltoonForm), ('information', UserInformationForm)]
    template_name = 'website/registergame.html'

    def done(self, form_list, form_dict, **kwargs):
        self.request.user.information.all().delete()
        self.request.user.soltoon.all().delete()

        soltoon = form_dict["soltoon"].save(commit=False)
        soltoon.user = self.request.user
        info = form_dict["information"].save(commit=False)
        info.user = self.request.user

        soltoon.save()
        info.save()

        return HttpResponseRedirect(reverse('soltoonwebsite_game'))

    def dispatch(self, request, *args, **kwargs):
        if (request.user.information.exists()) and (request.user.soltoon.exists()):
            return HttpResponseRedirect(reversed('soltoonwebsite_game'))
        return super().dispatch(request, *args, **kwargs)


@login_required
def upload_code(request):
    if not (request.method == 'POST'):
        return HttpResponseRedirect(reverse('soltoonwebsite_game'))

    code = UploadCodeForm(request.POST, request.FILES)
    if code.is_valid():
        codeModel = code.save(commit=False)
        codeModel.user = request.user
        codeModel.save()
    else:
        return

    return HttpResponseRedirect(reverse('soltoonwebsite_game'))
