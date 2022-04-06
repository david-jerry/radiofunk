from django.urls import path

from radio_funk.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    user_playlist,

    become_podcaster,
    do_not_become_podcaster
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("<str:username>/playlist/", view=user_playlist, name="playlist"),
    path("<str:username>/become_podcaster/", view=become_podcaster, name="podcaster"),
    path("<str:username>/become_listener/", view=do_not_become_podcaster, name="listener"),
]
