from django.http import HttpResponse
import random

from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from itertools import chain

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.http import require_http_methods


from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .models import Podcast, Episodes, Playlist
from radio_funk.users.models import User
from radio_funk.tunes.models import Stations

from radio_funk.utils.logger import LOGGER

# Create your views here.
class PodcastListview(ListView):
    model = Podcast
    allow_empty = True
    queryset = Podcast.managers.popular()
    template_name = "podcast/podcast.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_podcasts"] = Podcast.managers.popular()[:4]
        return context


podcast_list = PodcastListview.as_view()


class PodcastDetailview(DetailView):
    model = Podcast
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'podcast/podcast_detail.html'

podcast_detail = PodcastDetailview.as_view()


@require_http_methods(['POST', 'GET'])
@login_required
def create_playlist(request):
    user = request.user
    title = request.POST.get('ptitle')
    desc = request.POST.get('pdesc')
    p = request.POST.get('private')

    if p == "on":
        private = True
    else:
        private = False


    playlist = Playlist.objects.create(name=title,description=desc,owner=user,private=private)
    playlist.podcast.add()
    LOGGER.info(playlist.id)

    # add user to likes increasing it by 1
    user.playlist_likes.add(playlist.id)

    # get all user playlists
    playlists = user.playlist_author.all()

    return render(request, 'snippets/playlists.html', context={'playlists':playlists})

# @require_http_methods(['POST', 'GET', 'DELETE'])
@login_required
def delete_playlist(request, slug):
    playlist = get_object_or_404(Playlist, slug=slug)
    playlist.delete()
    playlists = request.user.playlist_author.all()
    context = {'user_playlists':playlists}
    return render(request, "snippets/pl.html", context)

@login_required
def delete_podcast(request, slug):
    podcast = get_object_or_404(Podcast, slug=slug)
    podcast.delete()
    podcasts = request.user.podcast_shows.all()
    context = {'user_podcasts':podcasts}
    return render(request, "snippets/pd.html", context)


@login_required
def remove_favorite(request, slug):
    podcast = get_object_or_404(Podcast, slug=slug)
    request.user.podcast_likes.remove(podcast.id)
    context = {
        "favorites": request.user.podcast_likes.all()
    }
    return render(request, "snippets/fav.html", context)

# @login_required
# def download_episode(request, slug, pslug):
#     ep = Episodes.managers.get(slug=slug, podcast__slug=pslug)
#     filename = ep.audio_file.name
#     response = HttpResponse(ep.audio_file, content_type='audio/mpeg')


@require_http_methods(['POST', 'GET'])
@login_required
def podcast_like(request, slug):
    podcast = Podcast.managers.get(slug=slug)
    user = request.user
    user.podcast_likes.add(podcast.id)
    return HttpResponse(f"""
        <button hx-post="/podcast/{podcast.slug}/like/" hx-swap="outerHTML" hx-target="this" @click="pof_{podcast.id} = true" :class="pof_{podcast.id} ? 'hidden' : ''" type="button" class="rounded-full px-4 border pt-1 leading-none border-black dark:border-white-200 text-2xl hover:bg-black dark:hover:bg-white-200 hover:text-white-200 dark:hover:text-black duration-200">
            Follow
        </button>
    """)



@require_http_methods(['POST', 'GET'])
@login_required
def podcast_unlike(request, slug):
    podcast = Podcast.managers.get(slug=slug)
    user = request.user
    user.podcast_likes.remove(podcast.id)
    return HttpResponse(f"""
        <button hx-post="/podcast/{podcast.slug}/unlike/" hx-swap="outerHTML" hx-target="this" @click="pof_{podcast.id} = false" :class="pof_{podcast.id} ? '' : 'hidden'" type="button" class="rounded-full px-4 border pt-1 leading-none border-black dark:border-white-200 text-2xl bg-black dark:bg-white-200 dark:hover:text-white-200 text-white-200 hover:text-black dark:text-black hover:bg-transparent dark:hover:bg-transparent duration-200">
            Unfollow
        </button>
    """)

class PlaylistDetail(DetailView):
    model = Playlist
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'users/playlist_detail.html'

playlist_detail = PlaylistDetail.as_view()


