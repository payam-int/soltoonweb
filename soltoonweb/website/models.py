from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class BlogPost(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, editable=False)
    status = models.BooleanField(verbose_name=_("published"))

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
