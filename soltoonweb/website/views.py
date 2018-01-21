from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, \
    PasswordResetConfirmView, PasswordResetDoneView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout, login
from django.utils.translation import ugettext_lazy as _

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, FormView, UpdateView
from formtools.wizard.views import SessionWizardView
from requests import post

from sandbox.models import Code, TrainingScenario, TrainingScenarioCode, UserProfile, Soltoon, CompetitionCode, \
    ExhibitionCompetition, Competition
from website.forms import EditProfileForm, SoltoonForm, UploadCodeForm, UploadScenraioCodeForm, SignupForm, \
    EditSoltoonForm, ExhibitionCompetitionForm, EnterEmailForm
from website.tokens import account_activation_token


class Home(TemplateView):
    template_name = 'website/home.html'

    def get(self, request):
        return render(request, self.template_name)


class Login(LoginView):
    template_name = 'website/login.html'
    redirect_authenticated_user = True

    def get(self, request):
        return render(request, self.template_name)

    def form_invalid(self, form):
        for e in form.errors:
            messages.error(self.request, _("Invalid login information."))
        return super().form_invalid(form)


class Logout(View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)

        return HttpResponseRedirect(reverse('soltoonwebsite_home'))


@method_decorator(login_required, 'dispatch')
class EditProfile(FormView):
    template_name = 'website/user_edit.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('soltoonwebsite_game')

    def get_form_kwargs(self):
        args = super().get_form_kwargs()

        i = UserProfile.objects.filter(user=self.request.user.id)

        if i.count() > 0:
            args['instance'] = i.get()

        return args

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.save()

        return super(EditProfile, self).form_valid(form)


@method_decorator(login_required, 'dispatch')
class EditSoltoon(FormView):
    template_name = 'website/soltoon_edit.html'
    form_class = EditSoltoonForm
    success_url = reverse_lazy('soltoonwebsite_game')

    def get_form_kwargs(self):
        args = super().get_form_kwargs()

        i = Soltoon.objects.filter(user=self.request.user.id)

        if i.count() > 0:
            args['instance'] = i.get()

        return args

    def form_valid(self, form):
        soltoon = form.save(commit=False)
        soltoon.user = self.request.user
        soltoon.save()

        return super(EditSoltoon, self).form_valid(form)


@method_decorator(login_required, 'dispatch')
class TrainingScenarios(TemplateView):
    template_name = 'website/training_scenarios.html'

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['scenarios'] = TrainingScenario.objects.all()
        c['user'] = self.request.user
        if not (self.request.user.information.exists()):
            messages.info(self.request, _("enter information before send"))
        else:
            print(self.request.user.information)

        return c


@method_decorator(login_required, 'dispatch')
class Game(FormView):
    template_name = 'website/competition.html'
    form_class = ExhibitionCompetitionForm
    success_url = reverse_lazy('soltoonwebsite_game')

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['competitions'] = Competition.objects.filter(competitors_code__user=self.request.user)

        return c

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.information.exists()):
            return HttpResponseRedirect(reverse('soltoonwebsite_edit_profile'))

        return super(Game, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        opp_code = form.cleaned_data['opponent'].code
        my_code = self.request.user.soltoon.get().code

        e = ExhibitionCompetition(creator=self.request.user)
        e.save()
        e.competitors_code.add(my_code, opp_code)
        e.save()

        return super().form_valid(form)


@method_decorator(login_required, 'dispatch')
class RegisterGame(SessionWizardView):
    form_list = [('soltoon', SoltoonForm), ('information', EditProfileForm)]
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


@method_decorator(login_required, 'dispatch')
class TrainingScenariosSubmittions(TemplateView):
    template_name = 'website/training_scenario_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submittions'] = TrainingScenarioCode.objects.filter(
            training_scenario=self.kwargs['scenario']).order_by(
            'created_at')
        return context


@method_decorator(login_required, 'dispatch')
class TrainingScenariosSendCode(FormView):
    template_name = 'website/training_send_code.html'
    form_class = UploadScenraioCodeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_scenario_id = self.kwargs['scenario']
        context['scenario'] = TrainingScenario.objects.get(pk=current_scenario_id)
        try:
            context['code'] = TrainingScenarioCode.objects.get(training_scenario_id=current_scenario_id,
                                                               user=self.request.user)
        except:
            context['code'] = None

        return context

    def form_valid(self, form):
        current_scenario = self.kwargs['scenario']
        TrainingScenarioCode.objects.filter(training_scenario_id=current_scenario, user=self.request.user).delete()
        new_code = form.save(commit=False)
        new_code.user = self.request.user
        new_code.training_scenario = TrainingScenario.objects.get(pk=current_scenario)
        new_code.save()

        return HttpResponseRedirect(reverse('soltoonwebsite_game_training_table', args=[current_scenario]))


@method_decorator(login_required, 'dispatch')
class CompetitionSendCode(FormView):
    template_name = 'website/game_send_code.html'
    form_class = UploadCodeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['code'] = CompetitionCode.objects.filter(user=self.request.user).order_by('-created_at').first()
        except Exception as e:
            context['code'] = None

        return context

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.soltoon):
            messages.error(self.request, _('You should config your soltoon.'))

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        if context['code']:
            context['code'].delete()

        new_code = form.save(commit=False)
        new_code.user = self.request.user
        new_code.save()

        soltoon = self.request.user.soltoon.get()
        soltoon.code = new_code
        soltoon.save()

        return HttpResponseRedirect(reverse('soltoonwebsite_game_send_code'))


class Signup(FormView):
    form_class = SignupForm
    template_name = 'website/signup.html'
    success_url = reverse_lazy('soltoonwebsite_home')

    def form_valid(self, form):
        user = form.save(commit=False)
        # user.is_active = False
        user.email = form.email
        user.save()
        login(self.request, user=user)
        self.send_activate_mail(user, form)
        return super(Signup, self).form_valid(form)

    def send_activate_mail(self, user, form):
        current_site = get_current_site(self.request)
        mail_subject = _('Activate your Soltoon account')
        context = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
        message = render_to_string('website/mail/signup_activate_mail.html', context)

        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()

        messages.success(self.request, _('User has been created. check your email for confirmation mail.'))


class ActivateUser(View):
    # template_name = 'website/activate_user.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(self.kwargs['uidb64']))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, self.kwargs['token']):
            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('soltoonwebsite_home'))

        return HttpResponse("ERROR.")


class PasswordReset(PasswordResetView):
    template_name = 'website/password_reset.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'website/password_reset_confirm.html'


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'website/password_reset_done.html'


@method_decorator(login_required, 'dispatch')
class EnterEmail(FormView):
    template_name = 'website/enter_email.html'
    form_class = EnterEmailForm
    success_url = reverse_lazy('soltoonwebsite_game')

    def form_valid(self, form):
        self.request.user.email = form.cleaned_data['email']
        self.request.user.save()

        return super().form_valid(form)
