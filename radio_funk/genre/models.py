import geocoder

from django.db.models import Q, Manager, Count, Max, Avg
from django.db.models import (
    CASCADE,
    DO_NOTHING,
    BooleanField,
    CharField,
)
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse


from autoslug import AutoSlugField
from tinymce import HTMLField
from model_utils.models import TimeStampedModel

from .managers import GenreManager

class Genre(TimeStampedModel):
    name = CharField(_("Genre Name"), max_length=255, blank=False, null=True, unique=True)
    slug = AutoSlugField(_("Slug"), populate_from="name", unique="True", null=True)
    color = CharField(_("Background Color"), blank=True, max_length=10)
    description = HTMLField(_('Genre Description'))

    active = BooleanField(default=True)

    objects = GenreManager()

    def __str__(self):
        return self.name.title()

    def get_most_popular(self):
        return self.podcast.all().annotate(podcast_count=Count("like")).order_by('podcast_count').first()

    def get_all_podcast(self):
        return self.podcast.all()

    def get_all_episodes(self):
        return self.episode.all()

    @property
    def get_podcast_count(self):
        return self.podcast.all().count()

    @property
    def get_episodes_count(self):
        return self.episode.all().count()

    class Meta:
        managed = True
        verbose_name = "Podcast & Radio Genre"
        verbose_name_plural = "Podcast & Radio Genres"
        ordering = ["-created"]

    def get_absolute_url(self):
        return reverse("genre_detail", kwargs={"slug": self.slug})

