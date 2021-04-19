from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="Index"),
    path("super_secret/", views.super_secret_site, name="Super secret site"),
    path("log_out/", views.log_out, name="Log out"),
]