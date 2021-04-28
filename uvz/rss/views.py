import time
import feedparser
from typing import Dict, List
from feedparser.util import FeedParserDict
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from uvz.utilities.decorators import validate_token_in_body, validate_request_body


class ParsedEntry(object):
    """Parsed RSS entry class"""

    def __init__(self, title: str, description: str, link: str, published: str, ) -> None:
        super().__init__()
        self.title: str = title
        self.description: str = description
        self.link: str = link
        self.published: str = published

    def toJSON(self) -> Dict[str, str]:
        serialized_dict = {
            "title": self.title,
            "description": self.description,
            "link": self.link,
            "published": self.published,
        }
        return serialized_dict

    def __str__(self) -> str:
        return str({
            "title": self.title,
            "description": self.description,
            "link": self.link,
            "published": self.published,
        })


class FeedParser(object):
    """Wrapper wich supports basic functionality for parsing RSS feed"""

    def __init__(self, feed: FeedParserDict) -> None:
        super().__init__()
        self.entries: List[ParsedEntry] = []
        for entry in feed["entries"]:
            self.entries.append(ParsedEntry(str(entry["title"]), str(
                entry["summary"]), str(entry["link"]), time.strftime('%Y-%m-%dT%H:%M:%SZ', time.strptime(" ".join(str(entry["published"]).split(" ")[1:-1]), "%d %b %Y %H:%M:%S")))
            )

    def getEntry(self, i: int) -> Dict[str, str]:
        if i > 9:
            return self.entries[-1].toJSON()
        return self.entries[i].toJSON()

@validate_request_body()
@require_http_methods(["POST", "GET"])
@validate_token_in_body
def get_lastest_rss_from_feed(request: HttpRequest):
    feed = feedparser.parse(
        "https://www.uvzsr.sk/index.php?option=com_content&view=frontpage&Itemid=1&type=rss&format=feed")
    feedparser_: FeedParser = FeedParser(feed)
    return JsonResponse(feedparser_.getEntry(0))


{
    'title': '175. VYHLÁŠKA a 176. VYHLÁŠKA Úradu verejného zdravotníctva Slovenskej republiky',
    'description': '<p align="justify" style="margin-top: 0px; margin-bottom: 0px;"><span style="font-size: 10pt; font-family: arial, helvetica, sans-serif;"><a href="https://www.uvzsr.sk/docs/info/ut/vyhlaska_175.pdf" target="_blank">175. VYHLÁŠKA Úradu verejného zdravotníctva Slovenskej republiky, ktorou sa nariaďujú opatrenia pri ohrození verejného zdravia k povinnosti prekrytia horných dýchacích ciest</a><span><br /><br /><span><a href="https://www.uvzsr.sk/docs/info/ut/vyhlaska_176.pdf" target="_blank">176. VYHLÁŠKA Úradu verejného zdravotníctva\xa0Slovenskej republiky, ktorou sa nariaďujú opatrenia pri ohrození verejného zdravia ku karanténnym povinnostiam osôb po vstupe na územie Slovenskej republiky</a><span></span></span></span></span></p>',
    'link': 'https://www.uvzsr.sk/index.php?option=com_content&view=article&id=4692:175-vyhlaka-a-176-vyhlaka-uradu-verejneho-zdravotnictva-slovenskej-republiky&catid=250:koronavirus-2019-ncov&Itemid=153',
    'published': '2021-04-15T17:55:48Z'
}
