from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from sandbox.models import TrainingScenario, TrainingScenarioCode, UserProfile, Soltoon

admin.site.register(TrainingScenario)
admin.site.register(TrainingScenarioCode)
admin.site.register(UserProfile)
admin.site.register(Soltoon)
