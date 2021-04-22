from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="Index"),
    path("console/", views.console, name="Super secret site"),
]