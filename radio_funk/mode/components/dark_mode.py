from django_unicorn.components import UnicornView#, QuerySetType
from radio_funk.mode.models import Mode
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

from radio_funk.utils.logger import LOGGER
# from radio_funk.utils.context_processors.context_data import ip

class DarkModeView(UnicornView):
    # modes: QuerySetType[Mode] = Mode.objects.none()

    # reactlike use effect
    # def mount(self):
    #     self.modes = Mode.objects.all()

    def ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
            return str(ip)
        else:
            if settings.PRODUCTION:
                ip = self.request.META.get('REMOTE_ADDR')
                return str(ip)
            else:
                ip = '8.8.8.8'
                return str(ip)

    def change_dark(self):
        # if we added an input field on the component we do this
        # Mode.objects.create(ip=self.ip, theme=self.theme)
        # else

        Mode.objects.get_or_create(ip=self.ip(), theme="dark")[0]
        messages.success(self.request, "Dark Mode Activated")
        # to populate the mode list if there was any
        # self.modes = Mode.objects.all()
        # then to clear the field so it returns to an empty input field
        # self.ip = '' and self.theme = ''

    def change_light(self):
        Mode.objects.get(ip=self.ip(), theme="dark").delete()[0]
        messages.error(self.request, "Dark Mode Deactivated")
        # to empty the mode list in a case of delete all
        # self.modes = Mode.objects.none()
