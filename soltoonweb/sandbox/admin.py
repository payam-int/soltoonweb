from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from sandbox.models import TrainingScenario, TrainingScenarioCode, UserProfile, Soltoon, CompetitionCode
from website.views import CompetitionSendCode

admin.site.register(TrainingScenario)
admin.site.register(TrainingScenarioCode)
admin.site.register(UserProfile)
admin.site.register(Soltoon)
admin.site.register(CompetitionCode)
