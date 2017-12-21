from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _


# Create your models here.

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

    file = models.FileField(verbose_name=_("file"), upload_to='userfiles/')
    file_type = models.CharField(verbose_name=_("file type"), choices=file_types, max_length=5)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, editable=False)
    status = models.IntegerField(verbose_name=_("status"), choices=code_status)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


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
    scheduled_for = models.DateTimeField()
    ready_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=competition_status)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


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
    competitors = models.ManyToManyField(to=Code, related_name='competitions')
    league = models.ForeignKey(to=League, related_name='competitions')


class Mission(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=40)
    description = models.TextField(verbose_name=_("description"))
    prerequisites = models.ManyToManyField(to='Mission')
    judge = models.ForeignKey(to='Code', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)


class MissionCompetition(Competition):
    competitor = models.ForeignKey(to=Code, on_delete=models.CASCADE, related_name='missions')
    mission = models.ForeignKey(to=Mission, on_delete=models.CASCADE, related_name='competitions')


class Achievement(models.Model):
    soltoon = models.ForeignKey('Soltoon', on_delete=models.CASCADE)
    mission = models.ForeignKey('Mission', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class UserInformation(models.Model):
    departments = (
        ("MCS", _("mathematical sciences")),
        ("CE", _("computer engineering"))
    )

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    student_id = models.IntegerField()
    department = models.CharField(max_length=40)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='information')


class Soltoon(models.Model):
    UNIFORMS = {
        0: '#ff00000',
        1: '#00ff000'
    }

    _uniforms = (
        (0, UNIFORMS[0]),
        (0, UNIFORMS[1]),
    )

    name = models.CharField(max_length=30)
    achievements = models.ManyToManyField(Mission, related_name='achieved_users', through=Achievement)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='soltoon')
    primary_uniform = models.IntegerField(choices=_uniforms)
    secondary_uniform = models.IntegerField(choices=_uniforms)


class CompetitionResult(models.Model):
    competition = models.ForeignKey(Competition, related_name='result')
    exit_code = models.IntegerField()
    result_json = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
