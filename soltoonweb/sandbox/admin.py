from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from sandbox.models import TrainingScenario, TrainingScenarioCode, UserProfile, Soltoon, CompetitionCode
from website.views import CompetitionSendCode

admin.site.register(TrainingScenario)
admin.site.register(TrainingScenarioCode)


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', 'student_id', 'ssn')


admin.site.register(UserProfile, admin_class=UserProfileAdmin)
admin.site.register(Soltoon)
admin.site.register(CompetitionCode)
