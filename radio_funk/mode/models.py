from django.db.models import (
    CASCADE,
    DO_NOTHING,
    BooleanField,
    CharField,
    DateField,
    DecimalField,
    FileField,
    ForeignKey,
    ImageField,
    IntegerField,
    OneToOneField,
    PositiveSmallIntegerField,
    UUIDField,
)
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel

# Create your models here.
class Mode(TimeStampedModel):
    DARK = "dark"
    LIGHT = "light"
    THEME = (
        (DARK, DARK),
        (LIGHT, LIGHT)
    )
    ip = CharField(max_length=500, blank=False, unique=True)
    theme = CharField(max_length=10, blank=False, choices=THEME, default=LIGHT)

    def __str__(self):
        return str(self.ip)

    class Meta:
        managed = True
        verbose_name = "Dark or Light Theme"
        verbose_name_plural = "Dark or Light Themes"
        ordering = ["-created"]

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)

