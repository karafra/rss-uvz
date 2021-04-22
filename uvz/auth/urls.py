from . import views
from django.urls import path


urlpatterns = [
    path("getToken/", views.get_token, name="Get auth token"), 
    path("validateToken/", views.validate_token, name="Validate auth token"),
    path("refreshToken/", views.refresh_token, name="Refresh auth token"),
]