from django.urls import path

from radio_funk.podcast.views import (
    search_view,
)

app_name = "podcast"
urlpatterns = [
    path("search/", view=search_view, name="search"),
]
