import inspect
import feedparser as fp
from datetime import datetime
from src.IService import IService
from typing import Any, List, TypedDict
from feedparser.util import FeedParserDict
from time import sleep, mktime, struct_time
from src.AbstractProcess import AbstractProcess


class RSSService(IService):
    FEED_URL: str = \
        "https://www.uvzsr.sk/index.php?option=com_content&view=frontpage&Itemid=1&type=atom&format=feed"

    class ParsedEntry(TypedDict):
        title: str
        link: str
        published_parsed: struct_time
        summary_detail:  str

    class _RSS_PROCESS(AbstractProcess):
        def _thread_function(self) -> None:
            """
            Continuously runs function supplied in target argument
            to construtor, and stores results in queue.
            """
            while True:
                if inspect.isgeneratorfunction(self.target):
                    rv: Any = next(self.target())
                    self.queue.put(rv)
                    continue
                rv = self.target()
                self.queue.put(rv)

    def __init__(self) -> None:
        super().__init__()

    def start_service(self):
        self.process = self._RSS_PROCESS(self.listen_for_updates)

    def stop_service(self):
        self.process._stop()

    def __load_entries(self) -> List[ParsedEntry]:
        """
        Function that loads rss entries from Úrad verejného zdravotníctva.
        This function also parses out the unnecessary parts of RSS records
        such as detailed descriptions, names of authors and/or time when it was updated.
        """
        feed: FeedParserDict = fp.parse(self.FEED_URL)
        out_dict: List[Any] = []
        for record in feed["entries"]:
            out_dict.append({
                "title": record["title"],
                "link": record["link"],
                "published_parsed": record["published_parsed"],
                "summary_detail": record["summary"]
            })
        return out_dict

    def listen_for_updates(self) -> None:
        """
        Listens for updates in rss feed. When the feed updated, sends mail to 
        all users specified in 'recievers' environment variable. Feed
        is refreshed every 10 seconds.
        :returns: None
        """
        LAST_PUBLISHED = datetime.now()
        last_rss_entry = self.__load_entries()[0]
        if datetime.fromtimestamp(mktime(last_rss_entry["published_parsed"])) < LAST_PUBLISHED:
            sleep(10)
            return
        LAST_PUBLISHED = datetime.now()
        yield last_rss_entry
