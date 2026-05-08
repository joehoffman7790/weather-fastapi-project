import random

import requests
from django.views.generic import TemplateView

class AboutUs(TemplateView):
    template_name = "aboutus.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['example'] = str(random.randint(1, 12))
        return context


class LatLong(TemplateView):
    template_name = "latlong.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = {"lat": kwargs["lat"], "lon": kwargs["lon"], "appid": '', "units": "imperial"}
        location = requests.get('https://api.openweathermap.org/data/2.5/weather', params=params).json()
        context.update({
            "name": location.get("name"),
            "state": location.get("state"),
            "country": location.get("country"),
            "lat": kwargs["lat"],
            "lon": kwargs["lon"],
            "feels_like": int(location['main']['feels_like']),
        })
        return context
