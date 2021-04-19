from . import views
from django.urls import path


urlpatterns = [
    path("getToken", views.get_token), 
    path("validateToken", views.validate_token),
]