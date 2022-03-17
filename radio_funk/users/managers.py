from django.db.models import Q, Manager, Count, Max, Avg
from django.db.models.query import QuerySet
from django.contrib.sites.models import Site
from django.contrib.auth.models import BaseUserManager

class UserQuerySet(QuerySet):
    """Returns managers for users."""


    def active(self):
        return self.filter(is_active=True)

    def podcaster(self):
        return self.active().filter(podcaster=False)

    def search(self, query=None):
        qs = self
        if query is not None:
            lookup = (
                Q(name__icontains=query) |
                Q(email__icontains=query) |
                Q(username__icontains=query)

            )
            qs = qs.podcaster().filter(lookup).distinct()
        return qs

    def latest(self):
        try:
            return self.podcaster().order_by("-date_joined")
        except IndexError:
            return None

    def popular(self):
        try:
            return self.podcaster().annotate(podcast_count=Count("follower")).order_by('podcast_count')
        except IndexError:
            return None

class UserObjManager(BaseUserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

    def active(self):
        return self.get_queryset().active()

    def podcaster(self):
        return self.get_queryset().podcaster()

    def latest(self):
        return self.get_queryset().latest()

    def popular(self):
        return self.get_queryset().popular()


