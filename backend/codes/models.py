from django.db import models
from django.contrib.auth.models import AbstractUser
from solo.models import SingletonModel
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator


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
    date_approved = models.DateTimeField(blank=True, null=True)
    language = models.IntegerField(choices=Languages.choices, default=Languages.JAVASCRIPT)
    is_example = models.BooleanField(default=False)
    duration_of_emulation_in_seconds = models.PositiveIntegerField(default=30, validators=[MinValueValidator(8)])
    generated_error = models.BooleanField(default=False)

    def __str__(self):
        return f'Code {self.id} {self.name}'


class AnimationPriorityQueueElement(models.Model):
    code = models.ForeignKey(Code, on_delete=models.CASCADE)
    priority = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])

    def pop_first():
        highest_priority_element = AnimationPriorityQueueElement.objects.order_by('-priority').first()
        AnimationPriorityQueueElement.objects.order_by('-priority').first().delete() 
        
        return highest_priority_element
        

class Config(SingletonModel):
    force_stop = models.BooleanField(default=False)
    force_run = models.BooleanField(default=False)
    udp_receive_run = models.BooleanField(default=False)
    udp_key = models.CharField(default='ABC123', max_length=8, validators=[MinLengthValidator(4)])

    animation_start_time = models.TimeField(blank=True, null=True)
    animation_end_time = models.TimeField(blank=True, null=True)
    last_raspberry_pi_update = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Code {self.id}'
