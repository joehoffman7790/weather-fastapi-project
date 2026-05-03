from django.contrib import admin

from weather.models import CurrentWeather, ForecastDay, Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "country_code", "owm_city_id", "last_queried")
    search_fields = ("name", "country_code")


@admin.register(CurrentWeather)
class CurrentWeatherAdmin(admin.ModelAdmin):
    list_display = ("location", "temp_c", "condition", "fetched_at")
    list_select_related = ("location",)


@admin.register(ForecastDay)
class ForecastDayAdmin(admin.ModelAdmin):
    list_display = ("location", "date", "temp_high_c", "temp_low_c", "condition")
    list_filter = ("date",)
    list_select_related = ("location",)
