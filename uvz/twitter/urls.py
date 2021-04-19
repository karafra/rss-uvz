from . import views
from django.urls.conf import path


urlpatterns = [
    path("makeTweet", views.make_tweet, name="Make tweet")   
]