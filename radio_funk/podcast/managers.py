from django.db.models import Q, Manager, Count, Max, Avg
from django.db.models.query import QuerySet
from django.contrib.sites.models import Site

class EpisodeQuerySet(QuerySet):
    """Returns public episodes that are currently activated."""


    def published(self):
        return self.exclude(published=None)

    def search(self, query=None):
        qs = self
        if query is not None:
            lookup = (
                Q(name__icontains=query) |
                Q(podcast__author__name__icontains=query) |
                Q(podcast__author__username__icontains=query) |
                Q(podcast__author_text__icontains=query) |
                Q(podcast__name__icontains=query) |
                Q(description__icontains=query)
            )
            qs = qs.published().filter(lookup).distinct()
        return qs

    def onsite(self, site=None):
        if not site:
            site = Site.objects.get_current()
        return self.filter(podcast__sites__name=site.name).distinct()

    def current(self):
        try:
            return self.published().order_by("-published")
        except IndexError:
            return None

    def popular(self):
        try:
            return self.published().annotate(podcast_count=Count("like")).order_by('podcast_count').order_by('name')
        except IndexError:
            return None


class EpManager(Manager):
    def get_queryset(self):
        return EpisodeQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

    def current(self):
        return self.get_queryset().current()

    def published(self):
        return self.get_queryset().published()

    def onsite(self):
        return self.get_queryset().onsite()

    def popular(self):
        return self.get_queryset().popular()


class PodcastQuerySet(QuerySet):
    """Returns shows that are on the current site."""
    def published(self):
        return self.filter(publish=True)

    def search(self, query=None):
        qs = self
        if query is not None:
            lookup = (
                Q(name__icontains=query) |
                Q(author__name__icontains=query) |
                Q(author__username__icontains=query) |
                Q(author_text__icontains=query) |
                Q(description__icontains=query)
            )
            qs = qs.published().filter(lookup).distinct()
        return qs

    def children(self):
        return self.published().filter(explicit=4)

    def onsite(self, site=None):
        if not site:
            site = Site.objects.get_current()
        return self.filter(sites__name=site.name).distinct()

    def popular(self):
        try:
            return self.published().annotate(podcast_count=Count("like")).order_by('podcast_count').order_by('name')
        except IndexError:
            return None

class PdManager(Manager):
    def get_queryset(self):
        return PodcastQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

    def published(self):
        return self.get_queryset().published()

    def popular(self):
        return self.get_queryset().popular()

    def onsite(self):
        return self.get_queryset().onsite()

    def children(self):
        return self.get_queryset().children()


class PlaylistQuerySet(QuerySet):
    """Returns public playlist."""


    def public(self):
        return self.filter(private=False)

    def search(self, query=None):
        qs = self
        if query is not None:
            lookup = (
                Q(name__icontains=query) |
                Q(owner__name__icontains=query) |
                Q(owner__username__icontains=query)
            )
            qs = qs.public().filter(lookup).distinct()
        return qs

    def popular(self):
        try:
            return self.public().annotate(podcast_count=Count("like")).order_by('podcast_count').order_by('name')
        except IndexError:
            return None

class PlaylistManager(Manager):
    def get_queryset(self):
        return PlaylistQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

    def public(self):
        return self.get_queryset().public()

    def popular(self):
        return self.get_queryset().popular()

