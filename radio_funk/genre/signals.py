import random
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from radio_funk.utils.logger import LOGGER

from .models import Genre

@receiver(pre_save, sender=Genre)
def bg_color_creator_signal(sender, instance, *args, **kwargs):
    if instance.color is None:
        instance.color = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
