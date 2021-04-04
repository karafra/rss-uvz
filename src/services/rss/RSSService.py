from typing import Any
import inspect
from threading import Thread
import feedparser as fp
from datetime import datetime
from src.IService import IService
from feedparser.util import FeedParserDict
import logging
from typing import Any, List, Optional, TypedDict
from time import sleep, mktime, struct_time
from src.AbstractProcess import AbstractProcess
import asyncio

class RSSService(IService):
    logger = logging.getLogger(__name__)

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
                    for value in self.target():
                        self.queue.put(value)
                        break
                self.queue.put(self.target())

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

    def listen_for_updates(self) -> Optional["ParsedEntry"]:
        """
        Listens for updates in rss feed. When the feed updated, sends mail to 
        all users specified in 'recievers' environment variable. Feed
        is refreshed every 10 seconds.
        :returns: None
        """
        LAST_PUBLISHED = datetime.now()
        last_rss_entry = self.__load_entries()[0]
        if datetime.fromtimestamp(mktime(last_rss_entry["published_parsed"])) > LAST_PUBLISHED:
            sleep(10)
            return None
        LAST_PUBLISHED = datetime.now()
        logging.info(f"Found new entry {last_rss_entry}")
        return last_rss_entry

    async def watch_rss(self):
        while True:
            if rv := self.process.queue.get():
                self.logger.info(f"New record found: {rv}")
                return rv 
            await asyncio.sleep(10)

if __name__ == "__main__":
    import threading

    def infinite_bg_loop():
        service: RSSService = RSSService()
        service.start_service()
        process: RSSService._RSS_PROCESS = service.process
        current_thread: Thread = threading.current_thread()
        while not getattr(current_thread, "stop_signal", False):
            if val := process.queue.get():
                print(val)
        service.stop_service()
        print(f"Stopped {threading.current_thread()}")

    th = threading.Thread(target=infinite_bg_loop)
    th.daemon = True
    th.start()
    while True:
        keyboard_input = input()
        if keyboard_input == "stop":
            print(f"Stoping {th} ...")
            th.__setattr__("stop_signal", True)
            th.join()
            print(f"Thread {th} joined with {threading.current_thread()}")
            break
            