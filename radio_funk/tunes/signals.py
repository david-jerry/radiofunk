# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver
# from django.contrib.gis.geos import Point

# from radio_funk.utils.logger import LOGGER

# from .models import Stations

# @receiver(post_save, sender=Stations)
# def radio_cordinate_post_save_signal(sender, created, instance, *args, **kwargs):
#     if created and (instance.lat and instance.long):
#         instance.location = Point(instance.long, instance.lat, srid=4326)
#         LOGGER.info("Created distance")
#     else:
#         instance.location = None
#         LOGGER.info("couldn't Create coordinates")

