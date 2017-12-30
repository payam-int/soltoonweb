import zipfile

from django.forms import ModelForm, FileField, forms, BooleanField, ImageField, FileInput, Select
from django.db import models

from sandbox.models import Soltoon, UserProfile, Code, TrainingScenarioCode
from django.conf import settings
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from website.widgets import ChooseUniformWidget


class SoltoonForm(ModelForm):
    class Meta:
        model = Soltoon
        exclude = ['achievements', 'user']


class EditProfileForm(ModelForm):
    avatar = ImageField(label=_("avatar"), required=False, widget=FileInput(attrs={'_no_label': False}))

    class Meta:
        model = UserProfile
        exclude = ['user']
        layout = [
            ('Two Fields', ('Field', 'first_name'), ('Field', 'last_name')),
            ('Three Fields', ('Field', 'ssn'), ('Field', 'student_id'), ('Field', 'enterance_year')),
            ('Field', 'department'),
            ('Field', 'avatar'),
        ]


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UploadCodeForm(ModelForm):
    def is_valid(self):
        if not (super(ModelForm, self).is_valid()):
            return False

        if self.cleaned_data['file_type'] == Code.ZIP:
            if not (zipfile.is_zipfile(self.cleaned_data['file'].file)):
                return False

        if self.cleaned_data['file'].size > settings.MAX_CODE_SIZE:
            return False

        return True

    class Meta:
        model = Code
        exclude = ['user', 'created_at', 'status']


class UploadScenraioCodeForm(ModelForm):
    def is_valid(self):
        if not (super(ModelForm, self).is_valid()):
            return False

        if self.cleaned_data['file_type'] == Code.ZIP:
            if not (zipfile.is_zipfile(self.cleaned_data['file'].file)):
                return False

        if self.cleaned_data['file'].size > settings.MAX_CODE_SIZE:
            return False

        return True

    class Meta:
        model = TrainingScenarioCode
        exclude = ['user', 'created_at', 'status', 'training_scenario']


class EditSoltoonForm(ModelForm):
    primary_uniform = forms.ChoiceField(label=_('primary uniform'), widget=ChooseUniformWidget(postfix='a'),
                                        choices=Soltoon._uniforms)
    secondary_uniform = forms.ChoiceField(label=_('secondary uniform'), widget=ChooseUniformWidget(postfix='b'),
                                          choices=Soltoon._uniforms)

    class Meta:
        model = Soltoon
        exclude = ['user', 'created_at', 'achievements', 'code']
        layout = [
            ('Field', 'name'),
            ('Two Fields',
             ('Field', 'primary_uniform'), ('Field', 'secondary_uniform'))
        ]
