from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass


class Languages(models.IntegerChoices):
    JAVASCRIPT = 0
    PYTHON = 1


class Code(models.Model):
    name = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    description = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    code = models.TextField(max_length=10000)
    approved = models.BooleanField(default=False)
    date_approved = models.DateTimeField(null=True)
    language = models.IntegerField(choices=Languages.choices, default=Languages.JAVASCRIPT)
    is_example = models.BooleanField(default=False)

    def __str__(self):
        return f'Code {self.id} {self.name}'
