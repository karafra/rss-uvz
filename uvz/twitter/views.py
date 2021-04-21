
from json import loads
from tweepy.api import API
from uvz.rss.views import ParsedEntry
from django.http.request import HttpRequest
from uvz.twitter.TwitterAPI import TwitterApi
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from uvz.utilities.decorators import validate_request_body, validate_token_in_body


TWITTER_API: API = TwitterApi()


@require_POST
@validate_request_body({
    "token": "Authentication token",
    "record": {
        "published": "Time the record was published",
        "link": "link to full article",
        "description": "Short description of article",
        "title": "Title of article",
    }
})
@validate_token_in_body
def make_tweet(request: HttpRequest):
    record = loads(request.body.decode("utf-8"))["record"]
    tweet = ParsedEntry(
        record["title"], record["description"], record["link"], record["published"])
    response = TWITTER_API.update_status(rss_tweet=tweet)
    return JsonResponse({
        # type: ignore
        "statusURL": f"https://twitter.com/{response.user.screen_name}/status/{response.id_str}"
    })
