from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Stations
from leaflet.admin import LeafletGeoAdmin

# Register your models here.
admin.site.register(Stations, LeafletGeoAdmin)
