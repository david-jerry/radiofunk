from django.db.models import Q, Manager, Count, Max, Avg
from django.db.models.query import QuerySet
from django.contrib.sites.models import Site

class GenreQuerySet(QuerySet):
    """Returns popular genres"""
    def active(self):
        return self.exclude(active=False)

    def popular(self):
        try:
            return self.active().annotate(podcast_count=Count("podcast")).order_by('podcast_count')
        except IndexError:
            return None


class GenreManager(Manager):
    def get_queryset(self):
        return GenreQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def popular(self):
        return self.get_queryset().popular()
