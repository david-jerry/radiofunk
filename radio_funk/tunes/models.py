import geocoder

from django.db import models
from django.conf import settings
from django.db.models import (
    CASCADE,
    DO_NOTHING,
    BooleanField,
    CharField,
    DateField,
    DecimalField,
    ManyToManyField,
    URLField,
    FileField,
    ForeignKey,
    ImageField,
    IntegerField,
    OneToOneField,
    PositiveSmallIntegerField,
    UUIDField,
)

from tinymce import HTMLField
from stdimage import StdImageField
from model_utils.models import TimeStampedModel
from countries_plus.models import Country as CountryField

mapbox_access_token = settings.MAPBOX_KEY

# Create your models here.
class Gift(TimeStampedModel):
    name = CharField(max_length=255, blank=False, unique=True)
    description = HTMLField('Gift Story')
    image = StdImageField(upload_to="gift/gif", blank=True, variations={'thumbnail': {"width": 100, "height": 100, "crop": True}})
    price = DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return self.name.title()


class Genre(TimeStampedModel):
    name = CharField(max_length=255, blank=False, null=True, unique=True)
    active = BooleanField(default=False)
    description = HTMLField('Genre Description')

    def __str__(self):
        return self.name.title()

class Tunes(TimeStampedModel):
    PODCAST = "Podcast"
    STATION = "Station"
    TYPE = (
        (PODCAST, 'Podcast'),
        (STATION, 'Station')
    )


    name = CharField(max_length=255, blank=False, null=True, unique=True)
    description = HTMLField('Tune Description')
    image = StdImageField(upload_to="tune/album_art", blank=True, variations={'thumbnail': {"width": 250, "height": 250, "crop": True}})
    mp3url = URLField(blank=False)
    country = ForeignKey(CountryField, on_delete=CASCADE, default="US")
    active = BooleanField(default=False)
    genre = ManyToManyField('Genre')
    tune_type = CharField(max_length=8, blank=True, null=True, choices=TYPE, default=STATION)
    creator = ForeignKey('users.User', related_name='creator', on_delete=DO_NOTHING)
    website = URLField(blank=True)

    address = models.TextField(default="P.O. Box 3000 Halifax, NS B3J 3E9")
    phone = CharField(max_length=14, blank=True, null=True, default="+(902) 420-8311")
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name.title()

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.address, key=mapbox_access_token)
        g = g.latlng  # returns => [lat, long]
        self.lat = g[0]
        self.long = g[1]
        return super(Tunes, self).save(*args, **kwargs)

class PodcastGift(TimeStampedModel):
    podcast = ForeignKey('Tunes', related_name='podcast', on_delete=DO_NOTHING)
    gift = ForeignKey('Gift', related_name='gift', on_delete=DO_NOTHING)
    sender = ForeignKey('users.User', related_name='gifter', on_delete=DO_NOTHING)

    def __str__(self):
        return f"{self.podcase.name.title()} Gifts"
