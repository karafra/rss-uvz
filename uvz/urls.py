"""uvz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from django.urls.conf import include

from .rss.urls import urlpatterns as url_rss
from .auth.urls import urlpatterns as url_auth
from .database.urls import urlpatterns as url_db
from .email.urls import urlpatterns as url_email
from .admin.urls import urlpatterns as url_admin
from .twitter.urls import urlpatterns as url_twitter


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/rss/", include(url_rss)),
    path("api/database/", include(url_db)),
    path("api/twitter/", include(url_twitter)), 
    path("api/email/", include(url_email)),
    path("api/auth/", include(url_auth)),
    path("", include(url_admin)),
]
