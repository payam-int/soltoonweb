from datetime import datetime

import sys
from PIL import Image
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import FileExtensionValidator
from django.db import models
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
import os
from django.utils import timezone

# Create your models here.
from io import BytesIO


class Code(models.Model):
    UPLOADED = 0
    COMPILED = 2
    COMPILING = 1
    ERROR_IN_COMPILE = -1

    code_status = (
        (0, _('uploaded')),
        (2, _('compiled')),
        (1, _('compiling')),
        (-1, _('error in compilation')),
    )

    RAR = "RAR"
    TAR_GZ = "TARGZ"
    ZIP = "ZIP"

    file_types = (
        ('TARGZ', ".tar.gz"),
        ('ZIP', ".zip"),
        ('RAR', ".rar"),
    )

    file = models.FileField(verbose_name=_("file"), upload_to='private_media/codes/',
                            validators=[FileExtensionValidator(['zip', 'rar', 'tar.gz', 'gz'])], )
    file_type = models.CharField(verbose_name=_("file type"), choices=file_types, max_length=5)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, editable=False)
    status = models.IntegerField(verbose_name=_("status"), choices=code_status, default=UPLOADED)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def filename(self):
        return os.path.basename(self.file.name)

    def status_display(self):
        for s in self.code_status:
            if self.status == s[0]:
                return s[1]
        return 'Undefined'

    def __str__(self):
        return "{0} - {1}".format(self.user.username, self.created_at)


class TrainingScenario(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=128)
    description = models.TextField(verbose_name=_("description"))
    creator = models.ForeignKey(to=User, on_delete=models.SET_NULL, editable=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    deadline = models.DateTimeField()

    def from_now_deadline(self):
        diff = int((self.deadline - timezone.now()).total_seconds())
        if (diff > 0):
            minutes = diff // 60 % 60
            hours = diff // 3600 % 24
            days = diff // (3600 * 24)

            return "{0} {1} {2} {3} {4} {5}".format(days, _("days"), hours, _("hours"), minutes, _("minutes"))
        return _("passed")

    def __str__(self):
        return self.name


class TrainingScenarioCode(Code):
    training_scenario = models.ForeignKey(to='TrainingScenario', on_delete=models.CASCADE,
                                          related_name='all_submittions')

    def __str__(self):
        return _("{0} by {1}").format(str(self.training_scenario), str(self.user))


class CodeError(models.Model):
    COMPILE_ERROR = -1
    DECOMPRESS_ERROR = -2

    error_types = (
        (-1, _("compile error")),
        (-2, _("decompress error")),
    )

    code = models.ForeignKey(to='Code', on_delete=models.CASCADE)
    error_code = models.IntegerField(choices=error_types)
    error_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class Competition(models.Model):
    SUBMITTED = 0
    RUNNING = 1
    READY = 3
    EXITED = 2
    ERROR = -1

    competition_status = (
        (0, _("submitted")),
        (1, _("running")),
        (2, _("exited")),
        (3, _("ready")),
        (-1, _("error")),
    )

    creator = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='competitions')
    scheduled_for = models.DateTimeField(auto_now=True)
    ready_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=competition_status, default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    competitors_code = models.ManyToManyField(to='Code', related_name='competition')


class ExhibitionCompetition(Competition):
    pass


class CompetitionCode(Code):
    pass


class CompetitionError(models.Model):
    competition = models.ForeignKey(to=Competition, on_delete=models.CASCADE, related_name='error')
    error_code = models.IntegerField()
    error_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class League(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=40)
    description = models.TextField(verbose_name=_("description"))
    judge = models.ForeignKey(to='Code', on_delete=models.SET_NULL, null=True)
    capacity = models.IntegerField()
    creator = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class LeagueCompetition(Competition):
    league = models.ForeignKey(to=League, related_name='competitions')


class Mission(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=40)
    description = models.TextField(verbose_name=_("description"))
    prerequisites = models.ManyToManyField(to='Mission')
    judge = models.ForeignKey(to='Code', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)


class MissionCompetition(Competition):
    mission = models.ForeignKey(to=Mission, on_delete=models.CASCADE, related_name='competitions')


class Achievement(models.Model):
    soltoon = models.ForeignKey('Soltoon', on_delete=models.CASCADE)
    mission = models.ForeignKey('Mission', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class UserProfile(models.Model):
    departments = (
        ("MCS", _("mathematical sciences")),
        # ("CE", _("computer engineering"))
    )

    default_avatar = static("sandbox/img/default-avatar.jpg")

    first_name = models.CharField(verbose_name=_("first name"), max_length=40)
    last_name = models.CharField(verbose_name=_("last name"), max_length=40)
    student_id = models.CharField(verbose_name=_("student id"), max_length=20)
    ssn = models.CharField(verbose_name=_("social security number"), max_length=20)

    department = models.CharField(verbose_name=_("department"), max_length=40, choices=departments)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='information')
    enterance_year = models.IntegerField(verbose_name=_("enterance year"))
    avatar = models.ImageField(verbose_name=_("avatar"), upload_to='media/avatars/', null=False,
                               default=default_avatar)

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def save(self):
        # Opening the uploaded image

        if not (self.avatar == self.default_avatar):
            im = Image.open(self.avatar)

            output = BytesIO()

            crop_size = min(im.size)
            print(int(im.size[0] / 2 - crop_size / 2))

            if not (im.size[0] == 100) or not (im.size[1] == 100):
                # Resize/modify the image
                im = im.crop(
                    (int(im.size[0] / 2 - crop_size / 2), int(im.size[1] / 2 - crop_size / 2),
                     int(im.size[0] / 2 + crop_size / 2),
                     int(im.size[1] / 2 + crop_size / 2))).resize((100, 100), Image.ANTIALIAS)

                # after modifications, save it to the output
                im.save(output, format='JPEG', quality=100)
                output.seek(0)

                # change the imagefield value to be the newley modifed image value
                self.avatar = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.avatar.name.split('.')[0],
                                                   'image/jpeg',
                                                   sys.getsizeof(output), None)
        super(UserProfile, self).save()


class Soltoon(models.Model):
    UNIFORMS = {
        0: '#011627',
        1: '#81131d',
        2: '#13817a',
        3: '#530a3a',
        4: '#212f05'
    }

    _uniforms = (
        (0, '#011627'),
        (1, '#81131d'),
        (2, '#13817a'),
        (3, '#530a3a'),
        (4, '#212f05')
    )

    name = models.CharField(verbose_name=_("soltoon name"), max_length=30)
    achievements = models.ManyToManyField(Mission, related_name='achieved_users', through=Achievement)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='soltoon')
    primary_uniform = models.IntegerField(verbose_name=_("primary uniform"), choices=_uniforms)
    secondary_uniform = models.IntegerField(verbose_name=_("secondary uniform"), choices=_uniforms)
    code = models.ForeignKey(to='CompetitionCode', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.user.information.get().full_name())


class CompetitionResult(models.Model):
    competition = models.ForeignKey(Competition, related_name='result')
    exit_code = models.IntegerField()
    result_json = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
