from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from sandbox.models import TrainingScenario



admin.site.register(TrainingScenario)