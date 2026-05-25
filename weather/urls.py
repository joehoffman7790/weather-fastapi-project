from django.urls import path

from . import views

app_name = "weather"

urlpatterns = [
    # API endpoints
    path("api/weather/", views.weather, name="weather"),
    path("api/searches/", views.search_history, name="search-history"),

    # HTMX dashboard
    path("", views.dashboard, name="dashboard"),
    path("search/", views.dashboard_search, name="dashboard-search"),
]