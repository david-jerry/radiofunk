from django.http import HttpResponse
import random

from django.shortcuts import render
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

podcast_list = PodcastListview.as_view()


class PodcastDetailview(DetailView):
    model = Podcast
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'snippets/podcast_detail.html'

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



@require_http_methods(['POST', 'GET'])
@login_required
def podcast_like(request, slug):
    podcast = Podcast.managers.get(slug=slug)
    user = request.user
    user.podcast_likes.add(podcast.id)
    return HttpResponse("""
        <svg class="block w-10 h-10 text-red-600 cursor-pointer" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd">
            </path>
        </svg>
    """)



@require_http_methods(['POST', 'GET'])
@login_required
def podcast_unlike(request, slug):
    podcast = Podcast.managers.get(slug=slug)
    user = request.user
    user.podcast_likes.remove(podcast.id)
    return HttpResponse("""
        <svg class="block w-10 h-10 text-red-600 cursor-pointer" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z">
            </path>
        </svg>
    """)

class PlaylistDetail(DetailView):
    model = Playlist
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'users/playlist_detail.html'

playlist_detail = PlaylistDetail.as_view()


