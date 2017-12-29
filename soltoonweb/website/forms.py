import zipfile

from django.forms import ModelForm, FileField, forms, BooleanField, ImageField, FileInput
from django.db import models

from sandbox.models import Soltoon, UserProfile, Code, TrainingScenarioCode
from django.conf import settings
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _



class SoltoonForm(ModelForm):
    class Meta:
        model = Soltoon
        exclude = ['achievements', 'user']


class EditProfileForm(ModelForm):
    avatar = ImageField(label=_("avatar"), required=False, widget=FileInput(attrs={'_no_label': False}))

    class Meta:
        model = UserProfile
        exclude = ['user']


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

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
