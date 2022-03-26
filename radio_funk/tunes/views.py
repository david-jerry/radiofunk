from django.http import HttpResponse
import random

from django.shortcuts import render
from django.db.models import Q
from itertools import chain
from django.contrib import messages

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.http import require_http_methods

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from radio_funk.podcast.models import Podcast, Episodes, Playlist
from radio_funk.users.models import User
from .models import Stations

from radio_funk.utils.logger import LOGGER

# Create your views here.
# def home(request):
#     radios = Tunes.objects.filter(tune_type=Tunes.radio)
#     radios = Tunes.objects.filter(tune_type=Tunes.STATION)

class RadioDetailview(DetailView):
    model = Stations

radio_detail = RadioDetailview.as_view()

@require_http_methods(['POST', 'GET'])
def radio_like(request, slug):
    radio = get_object_or_404(Stations, slug=slug)
    user = request.user
    user.radio_likes.add(radio.id)
    return HttpResponse(f"""
        <svg hx-post="/stations/{radio.slug}/like/" hx-swap="outerHTML" hx-target="this" @click="ro_{radio.id} = true" :class="ro_{radio.id} ? 'hidden' : 'block'" class=" w-6 h-6 text-red-600 cursor-pointer" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z">
            </path>
        </svg>
    """)


@require_http_methods(['POST', 'GET'])
def radio_unlike(request, slug):
    radio = get_object_or_404(Stations, slug=slug)
    user = request.user
    user.radio_likes.remove(radio.id)
    return HttpResponse(f"""
        <svg hx-post="/stations/{radio.slug}/unlike/" hx-swap="outerHTML" hx-target="this" @click="ro_{radio.id} = false" :class="ro_{radio.id} ? 'block' : 'hidden'" class=" w-6 h-6 text-red-600 cursor-pointer" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd">
            </path>
        </svg>
    """)

