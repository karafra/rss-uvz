from django.urls import path
from . import views


urlpatterns = [
    path("sendMail", views.test, name="GetLastestRSS"),
]