from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Gift, EpisodeGift, Podcast, Episodes, Playlist

# Register your models here.
admin.site.register(Gift)
admin.site.register(EpisodeGift)
admin.site.register(Podcast, LeafletGeoAdmin)
admin.site.register(Episodes)
admin.site.register(Playlist)

