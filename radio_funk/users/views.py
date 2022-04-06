from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test

from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, ListView, CreateView, DeleteView

from radio_funk.podcast.models import Playlist
from django.shortcuts import get_object_or_404, render

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.podcaster:
            podcasts = self.request.user.podcast_shows.all()
        else:
            podcasts = None
        context['user_playlists'] = self.request.user.playlist_author.all()
        context['user_podcasts'] = podcasts
        return context


user_detail_view = UserDetailView.as_view()

@login_required
def become_podcaster(request, username):
    user = get_object_or_404(User, username=username)
    user.podcaster = True
    user.save()
    return render(request, 'users/accept.html', {'object':user})

@login_required
def do_not_become_podcaster(request, username):
    user = get_object_or_404(User, username=username)
    user.podcaster = False
    user.save()
    return render(request, 'users/accept.html', {'object':user})


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class UserPlaylist(ListView, LoginRequiredMixin):
    model = User
    template_name = "users/playlist.html"
    # slug_field = "username"
    # slug_url_kwarg = "username"

    def get_queryset(self):
        slug = self.kwargs.get("username")
        return Playlist.objects.filter(owner__username=slug)

user_playlist = UserPlaylist.as_view()
