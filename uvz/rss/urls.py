from django.urls import path
from . import views


urlpatterns = [
    path("lastRecord", views.get_lastest_rss_from_feed, name="GetLastestRSS"),
]