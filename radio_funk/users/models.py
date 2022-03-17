from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    DO_NOTHING,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    FileField,
    ForeignKey,
    ManyToManyField,
    ImageField,
    IntegerField,
    OneToOneField,
    PositiveSmallIntegerField,
    UUIDField,
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from stdimage import StdImageField
from model_utils.models import TimeStampedModel
from countries_plus.models import Country
from django.utils.timezone import now

from .managers import UserObjManager

class User(AbstractUser):
    """
    Default custom user model for radio_funk.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    model_name="Users"

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    image = StdImageField(upload_to="user/passport", blank=True, variations={'thumbnail': {"width": 100, "height": 100, "crop": True}})
    paid = BooleanField(default=False)

    created = DateTimeField(default=now, editable=False)

    podcaster = BooleanField(default=False)

    follower = ManyToManyField("self", related_name="followers", symmetrical=False, default=None, blank=True)

    managers = UserObjManager()

    def __str__(self):
        return self.name.title() if self.name else self.username.title()

    @property
    def get_follower_count(self):
        return self.follower.all().count()

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

class Wallet(TimeStampedModel):
    user = OneToOneField("users.User", on_delete=CASCADE, related_name="wallet")
    balance = DecimalField(max_digits=20, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.name.title()} {self.balance}"

    class Meta:
        managed = True
        verbose_name = "Wallet Balance"
        verbose_name_plural = "Wallet Balances"
        ordering = ["-created"]


class Privacy(TimeStampedModel):
    user = OneToOneField(User, on_delete=CASCADE, related_name="userprivacypolicy")
    cookies_and_tracking = BooleanField(default=True, help_text="This is a must have integration to enable us provide you with proper services and security. They do not create any security bridge for you and can only be used to login, signout and even ensure your sessions are still working. You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    google_ads = BooleanField(default=True, help_text="These is an advertising and devlivey network service, aimed solely to provide advert placements based on your browser informations. permiting this allows us provide you with adverts directly on our site. Be ensured that this does not constitute any security risk to you. You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    social_account_integration = BooleanField(default=True, help_text="Facebook, Instagram, Twitter, Google Plus, Linkedin, these providers are integrated into the website to ensure we have proper informations to provide for our social influence and lead generation. We do not share these information for any other purpose other than statistical analysis. You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    personal_information = BooleanField(default=True, help_text="These are personal informations we collect to provide quality and personalised services to you. They include (First Name, Last Name, Phone Number, Social Accounts, Addresses, Photo). You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    commercial_information = BooleanField(default=True, help_text="These are informations we collect for commercial purposes and are used for analysis as well as providing accurate data statistics of our services usage. You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    identifiers = BooleanField(default=True, help_text="These are informations we collect to prevent fraud, do analysis as well as utilize cloud services. They include Email address, device identifiers (User IDs, IP and Location). You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    internet_or_other_electronic_network_activity_information = BooleanField(default=True, help_text="These are informations we collect regarding the user interactions within the website. With this information we can provide cloud services such as Content Delivery Networks for static/asset and media files. You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")

    def __str__(self):
        return f"{self.user.name.title()} privacy policy"

    class Meta:
        managed = True
        verbose_name = "User Privacy"
        verbose_name_plural = "User Privacies"
        ordering = [ "-created"]


class Settings(TimeStampedModel):
    NORM = "normal"
    HIFI = 'high'
    LOFI = 'low'
    BITRATE = (
        (NORM, NORM),
        (HIFI, HIFI),
        (LOFI, LOFI)
    )
    user = OneToOneField(User, on_delete=CASCADE, related_name="usersoundsettings")
    bit_rate = CharField(max_length=50, choices=BITRATE, default=NORM)

    def __str__(self):
        return f"{self.user.name.title()} sound setting"

    class Meta:
        managed = True
        verbose_name = "Sound Setting"
        verbose_name_plural = "Sound Settings"
        ordering = [ "-created"]

