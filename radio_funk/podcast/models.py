from __future__ import unicode_literals

import json
import os
import tempfile
from pydub import AudioSegment
from pathlib import Path
import glob

from urllib.request import urlopen
import geocoder

from django.contrib.gis.db.models import PointField, Manager as GeoManager
from django.contrib.gis.geos import Point
from django.core.files.uploadedfile import UploadedFile
from django.core.files.base import ContentFile, File

from countries_plus.models import Country as CountryField

from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.db.models import (
    CASCADE,
    DO_NOTHING,
    PROTECT,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
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
    SmallIntegerField,
    PositiveSmallIntegerField,
    PositiveIntegerField,
    UUIDField,
)

from tinymce import HTMLField
from stdimage import StdImageField
from model_utils.models import TimeStampedModel
from countries_plus.models import Country as CountryField
from autoslug import AutoSlugField

from radio_funk.utils.storages import get_episode_upload_folder, get_show_upload_folder, get_hi_audio_upload_folder, get_norm_audio_upload_folder, get_lo_audio_upload_folder
from radio_funk.genre.models import Genre
from radio_funk.utils.fields import  UUIDField

from .managers import EpManager, PdManager, PlaylistManager

mapbox_access_token = settings.MAPBOX_KEY

from radio_funk.utils.logger import LOGGER

User = settings.AUTH_USER_MODEL

# Create your models here.
# from pydub import AudioSegment
# from pathlib import Path
# import os, glob

# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver
# from django.core.files.uploadedfile import UploadedFile
# from django.core.files import File


# from .models import Episodes

# def convert_hi_audio_files(audio_file, target_filetype="mp3", content_type='audio/mpeg', bitrate="320k"):
#     # file_path = audio_file.temporary_file_path()
#     file_path = Path(audio_file)
#     # file_path = str(audio_file.path)

#     # original_extension = file_path.split('.')[-1]
#     mp3_converted_file = AudioSegment.from_mp3(file_path)

#     # new_path = file_path[:-3] + target_filetype
#     # LOGGER.info(new_path)

#     mp3 = mp3_converted_file.export(file_path, format=target_filetype, bitrate="320k")

#     converted_audiofile = File(
#                 file=open(mp3.name, 'rb'),
#                 name=Path(mp3.name)
#             )
#     converted_audiofile.name = Path(mp3.name).name
#     converted_audiofile.content_type = content_type
#     converted_audiofile.size = os.path.getsize(mp3.name)
#     LOGGER.info(mp3.name)
#     LOGGER.info(f"Hi_Fi Audio: {converted_audiofile.name} - {converted_audiofile.size}")
#     return mp3.name

# def convert_no_audio_files(audio_file, target_filetype="mp3", content_type='audio/mpeg', bitrate="128k"):
#     # file_path = audio_file.temporary_file_path()
#     file_path = Path(audio_file)
#     # file_path = str(audio_file.path)
#     LOGGER.info(f"Initial Filepath: {file_path}")

#     # original_extension = file_path.split('.')[-1]
#     mp3_converted_file = AudioSegment.from_mp3(file_path)

#     # new_path = file_path[:-3] + target_filetype
#     LOGGER.info(f"Converted MP#: {mp3_converted_file}")

#     mp3 = mp3_converted_file.export(file_path, format=target_filetype, bitrate="128k")

#     converted_audiofile = File(
#                 file=open(mp3.name, 'rb'),
#                 name=Path(mp3.name)
#             )
#     converted_audiofile.name = Path(mp3.name).name
#     converted_audiofile.content_type = content_type
#     converted_audiofile.size = os.path.getsize(mp3.name)
#     LOGGER.info(mp3.name)
#     LOGGER.info(f"Audio: {file_path} {converted_audiofile.name} - {converted_audiofile.size}")
#     return mp3.name

# def convert_lo_audio_files(audio_file, target_filetype="mp3", content_type='audio/mpeg', bitrate="40k"):
#     # file_path = audio_file.temporary_file_path()
#     file_path = Path(audio_file)
#     # file_path = str(audio_file.path)

#     # original_extension = file_path.split('.')[-1]
#     mp3_converted_file = AudioSegment.from_mp3(file_path)

#     # new_path = file_path[:-3] + target_filetype
#     # LOGGER.info(new_path)

#     mp3 = mp3_converted_file.export(file_path, format=target_filetype, bitrate="40k")

#     converted_audiofile = File(
#                 file=open(mp3.name, 'rb'),
#                 name=Path(mp3.name)
#             )
#     converted_audiofile.name = Path(mp3.name).name
#     converted_audiofile.content_type = content_type
#     converted_audiofile.size = os.path.getsize(mp3.name)
#     LOGGER.info(mp3.name)
#     LOGGER.info(f"Lo_Fi Audio: {converted_audiofile.name} - {converted_audiofile.size}")
#     return mp3.name



class Gift(TimeStampedModel):
    """Unique gift items created for the listeners to gift to podcasters on live shows"""

    name = CharField(max_length=255, blank=False, unique=True)
    description = HTMLField('Gift Story')
    image = StdImageField(upload_to="gift/gif", blank=True, variations={'thumbnail': {"width": 100, "height": 100, "crop": True}})
    price = DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return self.name.title()

    class Meta:
        managed = True
        verbose_name = "Gift Item"
        verbose_name_plural = "Gift Items"
        ordering = ["-created"]


class Podcast(TimeStampedModel):
    """
    A podcast show/playlist with many episodes
    """

    EXPLICIT_CHOICES = (
        (1, _("yes")),
        (2, _("no")),
        (3, _("clean")),
        (4, _("kids"))
    )
    uuid = UUIDField(_("id"), unique=True)
    genre = ManyToManyField(Genre, blank=True, related_name="podcast")
    publish = BooleanField(_("published"), default=True)
    sites = ManyToManyField(Site, verbose_name=_('Sites'))
    ttl = PositiveIntegerField(
        _("ttl"), default=1440,
        help_text=_("""``Time to Live,`` the number of minutes a channel can be
        cached before refreshing."""))

    author = ForeignKey(
        User, related_name="podcast_shows",
        verbose_name=_("owner"),
        on_delete=PROTECT,
        help_text=_("""Make certain the user account has a name and e-mail address."""))

    author_text = CharField(
        _("Featured Personalities"), max_length=255, help_text=_("""
            This tag contains the name of the person or company that is most
            widely attributed to publishing the Podcast and will be
            displayed immediately underneath the title of the Podcast.
            The suggested format is: 'email@example.com (Full Name)'
            but 'Full Name' only, is acceptable. Multiple authors
            should be comma separated."""))

    name = CharField(_("title"), max_length=255)
    slug = AutoSlugField(_("slug"), populate_from="name", unique="True")
    description = HTMLField('Show Description')
    subtitle = CharField(
        _("subtitle"), max_length=255,
        help_text=_("Looks best if only a few words, like a tagline."))

    image = StdImageField(upload_to=get_show_upload_folder, blank=True, variations={"cover":{"width": 700, "height": 700}, 'thumbnail': {"width": 240, "height": 240, "crop": True}}, help_text=_("""
                A podcast must have 700 x 700 pixel cover art in JPG or PNG
                format using RGB color space. See our technical spec for
                details. To be eligible for featuring on iTunes Stores,
                choose an attractive, original, and square JPEG (.jpg) or
                PNG (.png) image at a size of 1400x1400 pixels. The image
                will be scaled down to 50x50 pixels at smallest in iTunes.
                For reference see the <a
                href="http://www.apple.com/itunes/podcasts/specs.html#metadata">iTunes
                Podcast specs</a>.<br /><br /> For episode artwork to
                display in iTunes, image must be <a
                href="http://answers.yahoo.com/question/index?qid=20080501164348AAjvBvQ">
                saved to file's <strong>metadata</strong></a> before
                enclosure uploading!"""))


    country = ForeignKey(CountryField, on_delete=CASCADE, default="US")
    address = TextField(blank=True, null=True)

    explicit = PositiveSmallIntegerField(
        _("explicit"), choices=EXPLICIT_CHOICES,
        help_text=_("Audience this content should be shown to. Explicit determines this episode not being shown to viewers under 18 years of age."), default=2)

    lat = FloatField(blank=True, null=True)
    long = FloatField(blank=True, null=True)
    location = PointField(srid=4326, geography=True, blank=True, null=True)

    like = ManyToManyField(User, related_name="podcast_likes", default=None, blank=True)

    objects = GeoManager()

    managers = PdManager()

    enable_comments = BooleanField(default=True)

    def __str__(self):
        return self.name.title()

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.address, key=mapbox_access_token)
        g = g.latlng  # returns => [lat, long]
        self.lat = g[0]
        self.long = g[1]
        self.location = Point(self.long, self.lat, srid=4326)
        return super(Podcast, self).save(*args, **kwargs)

    class Meta:
        managed = True
        verbose_name = "Podcast Show"
        verbose_name_plural = "Podcast Shows"
        ordering = ["-created"]

    @property
    def get_like_count(self):
        return self.like.count()

    def get_share_url(self):
        return "http://{0}{1}".format(Site.objects.get_current(), self.get_absolute_url())

    def get_absolute_url(self):
        return reverse("podcast_detail", kwargs={"slug": self.slug})

    @property
    def latest_episode(self):
        try:
            return self.episode_set.published().order_by("-published")[0]
        except IndexError:
            return None


class Episodes(TimeStampedModel):
    """An individual episode and its unique attributes for a podcast"""

    # SIXTY_CHOICES = tuple((x, x) for x in range(60))
    # hours = SmallIntegerField(_("hours"), default=0)
    # minutes = SmallIntegerField(_("minutes"), default=0, choices=SIXTY_CHOICES)
    # seconds = SmallIntegerField(_("seconds"), default=0, choices=SIXTY_CHOICES)
    model_name="Episodes"

    uuid = UUIDField("ID", unique=True)
    podcast = ForeignKey(Podcast, on_delete=PROTECT, related_name="podcast")

    audio = FileField(_("AudioFile"), blank=True, upload_to=get_norm_audio_upload_folder, validators=[FileExtensionValidator(allowed_extensions=['mp3'])])
    # audio_min = FileField(_("AudioFile_lo"), blank=True, upload_to=get_lo_audio_upload_folder, validators=[FileExtensionValidator(allowed_extensions=['mp3'])])
    # audio_high = FileField(_("AudioFile_hi"), blank=True, upload_to=get_hi_audio_upload_folder, validators=[FileExtensionValidator(allowed_extensions=['mp3'])])

    name = CharField(_("title"), max_length=255, unique=True)
    slug = AutoSlugField(_("slug"), populate_from="name", unique="True")
    description = HTMLField('Episode Description')
    subtitle = CharField(_("subtitle"), max_length=255, help_text=_("Looks best if only a few words, like a tagline."))
    image = StdImageField(upload_to=get_episode_upload_folder, blank=True, variations={"cover":{"width": 700, "height": 700}, 'thumbnail': {"width": 240, "height": 240, "crop": True}}, help_text=_("""
                An episode must have 700 x 700 pixel cover art in JPG or PNG
                format using RGB color space. See our technical spec for
                details. To be eligible for featuring on iTunes Stores,
                choose an attractive, original, and square JPEG (.jpg) or
                PNG (.png) image at a size of 1400x1400 pixels. The image
                will be scaled down to 50x50 pixels at smallest in iTunes.
                For reference see the <a
                href="http://www.apple.com/itunes/podcasts/specs.html#metadata">iTunes
                Podcast specs</a>.<br /><br /> For episode artwork to
                display in iTunes, image must be <a
                href="http://answers.yahoo.com/question/index?qid=20080501164348AAjvBvQ">
                saved to file's <strong>metadata</strong></a> before
                enclosure uploading!"""))


    keywords = ManyToManyField(
        Genre,blank=True,
        related_name="episode",
        help_text=_("Select multiple genre from the list of predefined genres"))

    explicit = PositiveSmallIntegerField(
        _("explicit"), choices=Podcast.EXPLICIT_CHOICES,
        help_text=_("Audience this content should be shown to. Explicit determines this episode not being shown to viewers under 18 years of age."), default=1)

    enable_comments = BooleanField(default=True)

    like = ManyToManyField(User, related_name="podcast_episode_likes", default=None, blank=True)

    published = DateTimeField(_("published"), default=now, null=True, blank=True, editable=True)

    objects = EpManager()

    def __str__(self):
        return self.name.title()

    class Meta:
        managed = True
        verbose_name = "Podcast Episode"
        verbose_name_plural = "Podcast Episodes"
        ordering = ["-created"]

    # def clean(self):
    #     super().clean()
    #     ext = self.audio.name[len(self.audio.name) - 4:]
    #     file = self.audio.file
    #     file.__class__
    #     if ext != ".mp3" or ext != ".wav":
    #         raise ValidationError(_("Warning, wrong file format"))
    #     else:
    #         convert_no_audio_files(file)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     file = self.audio.path
    #     file.__class__
    #     # new_name = f"{self.slug}.mp3"
    #     # with open(file) as f:
    #     audio = convert_no_audio_files(file)
    #     self.audio.save(audio, ContentFile(file))
    #     audio_hi = convert_hi_audio_files(file)
    #     self.audio_high.save(audio_hi, ContentFile(file))
    #     audio_lo = convert_lo_audio_files(file)
    #     self.audio_min.save(audio_lo, ContentFile(file))

    @property
    def get_gift_count(self):
        return self.episodegift_set.all().count()

    @property
    def get_like_count(self):
        return self.like.count()

    def get_absolute_url(self):
        return reverse("podcast_episode_detail",
                       kwargs={"podcast_slug": self.podcast.slug, "slug": self.slug})

    def get_next(self):
        next = self.__class__.objects.filter(published__gt=self.published)
        try:
            return next[0]
        except IndexError:
            return False

    def get_prev(self):
        prev = self.__class__.objects.filter(published__lt=self.published).order_by("-published")
        try:
            return prev[0]
        except IndexError:
            return False

    def get_share_url(self):
        return "http://{0}{1}".format(Site.objects.get_current(), self.get_absolute_url())


    def get_share_title(self):
        return self.title

    def get_share_description(self):
        return "{0}...".format(self.description[:512])

    def is_show_published(self):
        if self.podcast.published:
            return True
        return False




class EpisodeGift(TimeStampedModel):
    episode = ForeignKey('Episodes', related_name='episode_gift', on_delete=DO_NOTHING)
    gift = ForeignKey('Gift', related_name='gift', on_delete=DO_NOTHING)
    sender = ForeignKey('users.User', related_name='gifter', on_delete=DO_NOTHING)

    def __str__(self):
        return f"{self.episode.name.title()} Gifts from {self.sender.username.title()}"

    class Meta:
        managed = True
        verbose_name = "Episode Gift"
        verbose_name_plural = "Episode Gifts"
        ordering = ["-created"]




class Playlist(TimeStampedModel):
    """
    Playlist for multiple podcasts

    Fields: Name
            Podcast
            Created
            Modified
    """
    name = CharField(max_length=255, blank=False, unique=True)
    slug = AutoSlugField(_("slug"), populate_from="name", unique="True")
    description = HTMLField(_('Playlist Description'))
    owner = ForeignKey(User, on_delete=DO_NOTHING, related_name="playlist_author")
    podcast = ManyToManyField(Podcast)

    private = BooleanField(default=False)

    like = ManyToManyField(User, related_name="playlist_likes", default=None, blank=True)

    objects = PlaylistManager()

    def __str__(self):
        return str(self.name.title())

    class Meta:
        managed = True
        verbose_name = "Podcast Playlist"
        verbose_name_plural = "Podcast Playlists"
        ordering = ["-created"]

    @property
    def get_like_count(self):
        return self.like.count()




























