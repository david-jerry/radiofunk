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
@require_http_methods(['POST', 'GET'])
def search_view(request):
    template_name = "snippets/search.html"
    paginate_by = 20
    count = 0
    qs_lookup = None

    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    rgb = [r,g,b]

    hexa = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])


    query = request.POST.get('q', None)
    if query is not None:
        ep_res = Episodes.objects.search(query=query)
        rd_res = Stations.managers.search(query=query)
        pd_res = Podcast.managers.search(query=query)
        usr_res = User.managers.search(query=query)
        pl_res = Playlist.objects.search(query=query)
        qs_lookup = sorted(chain(
                            usr_res,
                            rd_res,
                        ), key=lambda instance:instance.created, reverse = True)[:4]
        count = len(qs_lookup)
    else:
        qs_lookup = None
        count = 0

    context = {
        'count': count,
        'query': query,
        'episodes': ep_res,
        'stations': rd_res,
        'podcasts': pd_res,
        'playlist': pl_res,
        'podcasters': usr_res,
        'object_list': qs_lookup,
    }
    return render(request, template_name, context)
