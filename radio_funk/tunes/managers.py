from django.db.models import Q, Manager, Count, Max, Avg
from django.db.models.query import QuerySet
from django.contrib.sites.models import Site
from django.contrib.gis.db.models.functions import GeometryDistance

class RadioQuerySet(QuerySet):
    """Returns managers for radio stations."""

    def active(self):
        return self.exclude(active=False)

    def search(self, query=None):
        qs = self
        if query is not None:
            lookup = (
                Q(name__icontains=query) |
                Q(creator__name__icontains=query)
            )
            qs = qs.active().filter(lookup).distinct()
        return qs

    def country(self, query=None):
        qs = self
        if query is not None:
            qs = qs.active().filter(country__name__icontains=query).distinct()
        return qs

    def other_radios(self, query=None):
        qs = self
        if query is not None:
            qs = qs.active().exclude(country__name__icontains=query).distinct()
        return qs

    def closest(self, dist=None, cur_loc=None):
        qs = self
        if cur_loc is not None and dist is not None:
            qs = qs.active().filter(location__dwithin = (cur_loc, dist)).annotate(distance=GeometryDistance("location", cur_loc)).order_by("distance").order_by("-created").distinct()
        return qs

    def latest(self):
        try:
            return self.active().order_by("-created")[:5]
        except IndexError:
            return None

    def popular(self, dist, cur_loc):
        try:
            return self.closest(dist, cur_loc).annotate(podcast_count=Count("like")).order_by('podcast_count')
        except IndexError:
            return None


class RadioManager(Manager):
    def get_queryset(self):
        return RadioQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

    def country(self, query=None):
        return self.get_queryset().country(query=query)

    def other_radios(self, query=None):
        return self.get_queryset().country(query=query)

    def active(self):
        return self.get_queryset().active()

    def latest(self):
        return self.get_queryset().latest()

    def popular(self, cur_loc, dist):
        return self.get_queryset().popular(cur_loc=cur_loc, dist=dist)

    def closest(self, cur_loc, dist):
        return self.get_queryset().closest(cur_loc=cur_loc, dist=dist)


