from django.contrib import admin
from .models import Tunes, Genre, Gift, PodcastGift

# Register your models here.
admin.site.register(Tunes)
admin.site.register(Genre)
admin.site.register(Gift)
admin.site.register(PodcastGift)
