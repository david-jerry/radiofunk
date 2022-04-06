from django.db.models import Q, Manager, Count, Max, Avg
from django.db.models.query import QuerySet
from django.contrib.sites.models import Site
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserQuerySet(QuerySet):
    """Returns managers for users."""


    def active(self):
        return self.filter(is_active=True)

    def podcaster(self):
        return self.active().filter(podcaster=True)

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
            return self.podcaster().annotate(podcast_count=Count("follower")).order_by('podcast_count').order_by('name')
        except IndexError:
            return None

class UserObjManager(Manager):
    # def create_user(self, email, password, **extra_fields):
    #     """
    #     Create and save a User with the given email and password.
    #     """
    #     if not email:
    #         raise ValueError(_('The Email must be set'))
    #     email = self.normalize_email(email)
    #     user = self.model(email=email, **extra_fields)
    #     user.set_password(password)
    #     user.save()
    #     return user

    # def create_superuser(self, email, password, **extra_fields):
    #     """
    #     Create and save a SuperUser with the given email and password.
    #     """
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)
    #     extra_fields.setdefault('is_active', True)

    #     if extra_fields.get('is_staff') is not True:
    #         raise ValueError(_('Superuser must have is_staff=True.'))
    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError(_('Superuser must have is_superuser=True.'))
    #     return self.create_user(email, password, **extra_fields)

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


