from decimal import Decimal
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model

from django.dispatch import receiver

from .models import Wallet, Privacy, Settings

from radio_funk.utils.logger import LOGGER

User = get_user_model()

@receiver(post_save, sender=User)
def user_post_save_signal(sender, created, instance, *args, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
        Privacy.objects.create(user=instance)
        Settings.objects.create(user=instance)
        LOGGER.info("Sent Registration Email to admin")
