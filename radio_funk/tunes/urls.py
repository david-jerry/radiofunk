from django.urls import path

from radio_funk.tunes.views import (
    radio_like,
    radio_unlike,
    radio_detail,
)

app_name = "radio"
urlpatterns = [
    path("<slug>/", view=radio_detail, name="radio_detail"),
    # radio like and unlike
    path("<slug>/like/", view=radio_like, name="radio_like"),
    path("<slug>/unlike/", view=radio_unlike, name="radio_unlike"),
]
