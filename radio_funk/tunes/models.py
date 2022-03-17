import geocoder

from django.db import models
from django.conf import settings
from django.contrib.gis.db.models import PointField, Manager as GeoManager
from django.contrib.gis.geos import Point
from django.db.models import (
    CASCADE,
    DO_NOTHING,
    BooleanField,
    CharField,
    DateField,
    DecimalField,
    ManyToManyField,
    URLField,
    TextField,
    FloatField,
    FileField,
    ForeignKey,
    ImageField,
    IntegerField,
    OneToOneField,
    PositiveSmallIntegerField,
    UUIDField,
)
from radio_funk.utils.storages import get_radio_upload_folder

from tinymce import HTMLField
from stdimage import StdImageField
from model_utils.models import TimeStampedModel
from countries_plus.models import Country as CountryField

from radio_funk.genre.models import Genre
from .managers import RadioManager

mapbox_access_token = settings.MAPBOX_KEY

User = settings.AUTH_USER_MODEL

# Create your models here.
class Stations(TimeStampedModel):
    model_name="Stations"

    name = CharField(max_length=255, blank=False, null=True, unique=True)
    description = HTMLField('Tune Description')
    logo = StdImageField(upload_to=get_radio_upload_folder, blank=True, variations={'thumbnail': {"width": 250, "height": 250, "crop": True}})
    stream_url = URLField(blank=False)
    genre = ManyToManyField(Genre, blank=True)

    creator = ForeignKey('users.User', related_name='creator', on_delete=DO_NOTHING)
    website = URLField(blank=True)

    country = ForeignKey(CountryField, on_delete=CASCADE, default="US")
    address = TextField(blank=True, null=True)
    phone = CharField(max_length=20, blank=True, null=True, default="+(902) 420-8311")

    lat = FloatField(blank=True, null=True)
    long = FloatField(blank=True, null=True)
    location = PointField(srid=4326, geography=True, blank=True, null=True)

    active = BooleanField(default=False)

    like = ManyToManyField(User, related_name="radio_likes", default=None, blank=True)

    objects = GeoManager()
    managers = RadioManager()

    def __str__(self):
        return self.name.title()

    class Meta:
        managed = True
        verbose_name = "Radio Upload"
        verbose_name_plural = "Radio Uploads"
        ordering = ["-created"]

    @property
    def get_like_count(self):
        return self.like.count()

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.address, key=mapbox_access_token)
        g = g.latlng  # returns => [lat, long]
        self.lat = g[0]
        self.long = g[1]
        self.location = Point(self.long, self.lat, srid=4326)
        return super(Stations, self).save(*args, **kwargs)

