from django.http import HttpResponse
import random

from django.shortcuts import render
from django.db.models import Q
from itertools import chain

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.http import require_http_methods


from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from radio_funk.podcast.models import Podcast, Episodes, Playlist
from radio_funk.users.models import User
from radio_funk.tunes.models import Stations
from radio_funk.genre.models import Genre

from radio_funk.utils.logger import LOGGER

class GenreDetailView(DetailView):
    model = Genre
    template = "genre/detail.html"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return Genre.objects.active().filter(slug=slug).distinct()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        context["podcasts"] = Podcast.managers.published().filter(genre__slug=slug)
        return context


genre_detail = GenreDetailView.as_view()

# @require_http_methods(['POST', 'GET'])
class ExploreView(ListView):
    model = Podcast
    template_name = "pages/search.html"

    def get_queryset(self):
        Podcast.managers.popular()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_podcaster"] = User.managers.popular()[:20]
        context["popular_genre"] = Genre.objects.popular()
        return context





# @require_http_methods(['GET', 'POST'])
def search_view(request):
    template_name = "snippets/search.html"
    count = 0
    qs_lookup = None

    query = request.GET.get('q')

    if query is not None:
        ep_res = Episodes.objects.search(query=query)
        pd_res = Podcast.managers.search(query=query)
        usr_res = User.managers.search(query=query)
        if request.user.is_authenticated:
            pl_res = Playlist.objects.search(query=query)
            qs_lookup = sorted(chain(ep_res, pd_res, usr_res, pl_res), key=lambda instance:instance.created, reverse = True)[:20]
        else:
            pl_res = None
            qs_lookup = sorted(chain(ep_res, pd_res, usr_res), key=lambda instance:instance.created, reverse = True)[:20]
        count = len(qs_lookup)


    popular_podcaster = User.managers.popular()[:20]
    popular_genre = Genre.objects.popular()

    context = {
        'count': count,
        'query': query,

        'episodes': ep_res[:30],
        'podcasts': pd_res[:30],

        'playlists': pl_res[:30] if pl_res is not None else None,
        'podcasters': usr_res[:20],

        'object_list': qs_lookup,

        "popular_podcaster": popular_podcaster,
        "popular_genre": popular_genre,
    }
    return render(request, template_name, context)
