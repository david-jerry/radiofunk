from django.utils import timezone
from django.conf import settings
import json
from radio_funk.tunes.models import Tunes, Genre


def context_data(request):
    all_radios = Tunes.objects.filter(tune_type=Tunes.STATION).order_by("created")
    # json_radios = json.dump(all_radios)
    radios = Tunes.objects.filter(tune_type=Tunes.STATION).order_by("created")[:8]
    podcasts = Tunes.objects.filter(tune_type=Tunes.PODCAST).order_by("created")[:8]
    genres = Genre.objects.filter(active=True).order_by("name")[:7]
    # if request.user.is_authenticated:
    #     transactions = Transactions.objects.filter(user=request.user)[:20]
    # else:
    #     transactions = None
    return {
        'radios':radios,
        'podcasts':podcasts,
        'genres':genres,
        'all_radios': all_radios,

        "settings": settings
    }


