from datetime import timedelta

from django.db import models
from django.utils import timezone

CURRENT_TTL = timedelta(minutes=10)
FORECAST_TTL = timedelta(hours=1)


class Location(models.Model):
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=2, blank=True)
    owm_city_id = models.IntegerField(unique=True, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    last_queried = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("name", "country_code")]

    def __str__(self) -> str:
        return f"{self.name}, {self.country_code}"


class CurrentWeather(models.Model):
    location = models.OneToOneField(
        Location,
        on_delete=models.CASCADE,
        related_name="current",
    )
    temp_c = models.FloatField()
    feels_like_c = models.FloatField()
    humidity = models.IntegerField()
    wind_speed_ms = models.FloatField()
    condition = models.CharField(max_length=50)
    condition_icon = models.CharField(max_length=10)
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Current weather for {self.location}"

    def is_stale(self) -> bool:
        return timezone.now() - self.fetched_at > CURRENT_TTL

    @property
    def temp_f(self) -> float:
        return self.temp_c * 9 / 5 + 32

    @property
    def feels_like_f(self) -> float:
        return self.feels_like_c * 9 / 5 + 32

    @property
    def wind_speed_mph(self) -> float:
        return self.wind_speed_ms * 2.237


class ForecastDay(models.Model):
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="forecast_days",
    )
    date = models.DateField()
    temp_high_c = models.FloatField()
    temp_low_c = models.FloatField()
    condition = models.CharField(max_length=50)
    condition_icon = models.CharField(max_length=10)
    fetched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("location", "date")]
        ordering = ["date"]

    def __str__(self) -> str:
        return f"{self.location} on {self.date}"

    def is_stale(self) -> bool:
        return timezone.now() - self.fetched_at > FORECAST_TTL

    @property
    def temp_high_f(self) -> float:
        return self.temp_high_c * 9 / 5 + 32

    @property
    def temp_low_f(self) -> float:
        return self.temp_low_c * 9 / 5 + 32


class SearchHistory(models.Model):
    SEARCH_TYPE_CHOICES = [
        ("city", "City"),
        ("coordinates", "Coordinates"),
    ]

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="searches",
    )
    search_type = models.CharField(max_length=20, choices=SEARCH_TYPE_CHOICES)
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-searched_at"]

    def __str__(self) -> str:
        return f"{self.location} ({self.search_type}) at {self.searched_at:%Y-%m-%d %H:%M}"
