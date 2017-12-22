import zipfile

from django.forms import ModelForm, FileField

from sandbox.models import Soltoon, UserInformation, Code
from soltoonweb import settings


class SoltoonForm(ModelForm):
    class Meta:
        model = Soltoon
        exclude = ['achievements', 'user']


class UserInformationForm(ModelForm):
    class Meta:
        model = UserInformation
        exclude = ['user']


class UploadCodeForm(ModelForm):
    def is_valid(self):
        if not (super(ModelForm, self).is_valid()):
            return False

        if self.cleaned_data['file_type'] == Code.ZIP:
            if not(zipfile.is_zipfile(self.cleaned_data['file'].file)):
                return False

        if self.cleaned_data['file'].size > settings.MAX_CODE_SIZE:
            return False

        return True

    class Meta:
        model = Code
        exclude = ['user', 'created_at', 'status']
