from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="Index"),
    path("console/", views.console, name="Super secret site"),
    path("log_out/", views.log_out, name="Log out"),
    path("resfreshToken", views.refreshToken),
]