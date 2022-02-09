import json
from datetime import timezone
from decimal import Decimal

import requests
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

# from requests_html import HTMLSession
from radio_funk.utils.logger import LOGGER
from radio_funk.tunes.models import Genre, Tunes

User = get_user_model()

host = settings.RADIO_HOST
api = settings.RADIO_API

class Command(BaseCommand):
    help = _("Collect Radio Station Data")

    def handle(self, *args, **kwargs):
        url = "https://radio-world-50-000-radios-stations.p.rapidapi.com/v1/radios/getTopByCountry"

        headers = {
            'x-rapidapi-host': host,
            'x-rapidapi-key': api
        }
        datum = {"query":"us"}
        x = requests.request("GET", url, params=datum, headers=headers)
        if x.status_code != 200:
            return str(x.status_code)

        results = x.json()
        for i in results['radios']:
            image = i[0][0]["basic"]

        Tunes.objects.create(name=name, image=image,  mp3url=url, genre=[genre], tune_type=Tunes.STATION, creator=1, active=True, country=country.upper())

        self.stdout.write("Exchange Rate Retrieved Successfully.")
