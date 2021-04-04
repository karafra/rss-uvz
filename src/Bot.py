import asyncio
import logging
from os import environ
from time import sleep
from dotenv import load_dotenv
from src.IService import IService
from typing import Dict, Literal, Optional, Union
from src.services.rss.RSSService import RSSService
from src.services.email.EmailService import EmailService
from src.services.tweet.TwitterService import TweetObject, TwitterService

class Config(object):
    SERVICES: Dict[Literal["email", "tweet", "rss"], bool]

class Config1(Config):
    SERVICES = {
        "email": True,
        "tweet": False,
        "rss": True,
    }

class Bot(object):

    def __init__(self, config: Optional[Config] = None) -> None:
        load_dotenv()
        self.config: Optional[Config] = config
        self.__logger = logging.getLogger(__name__)
        self.__email_service: Optional[EmailService] = None
        self.__rss_service: Optional[RSSService] = None
        self.__tweet_service: Optional[TwitterService] = None

    def __start_email_service(self) -> None:
        self.__logger.info("Email service starting ...")
        service_: IService = EmailService(
            environ["PERSONAL_MAIL"], environ["PERSONAL_MAIL_PASSWORD"])
        self.__email_service = service_
        service_.start_service()
        self.__logger.info("Email service started")

    def __start_rss_service(self) -> None:
        self.__logger.info("RSS service starting ...")
        service_: IService = RSSService()
        self.__rss_service = service_
        service_.start_service()
        self.__logger.info("RSS service started")

    def __start_tweet_service(self) -> None:
        self.__logger.info("Tweet service starting ...")
        service_: IService = TwitterService()
        service_.start_service()
        self.__tweet_service = service_
        self.__logger.info("Tweet service started")

    def start_service(self, service: Union[Literal["email", "rss", "tweet"], str]) -> None:
        """Start service supported by bot."""
        if service == "email":
            self.__start_email_service()
        elif service == "rss":
            self.__start_rss_service()
        elif service == "tweet":
            self.__start_tweet_service()
        else:
            self.__logger.error("Unsupported service")

    def __stop_email_service(self) -> None:
        self.__logger.info("Email service stoping ...")
        self.__email_service.stop_service()
        self.__logger.info("Email service stoped")

    def __stop_rss_service(self) -> None:
        self.__logger.info("RSS service stoping ...")
        self.__rss_service.stop_service()
        self.__logger.info("RSS service stoped")

    def __stop_twiter_service(self) -> None:
        self.__logger.info("Tweet service stoping ...")
        self.__tweet_service.stop_service()
        self.__logger.info("Tweet service stoped")

    def stop_service(self, service: Union[Literal["email", "rss", "tweet"], str]) -> None:
        """Stop service supported by bot."""
        if service == "email":
            self.__stop_email_service()
        elif service == "rss":
            self.__stop_rss_service()
        elif service == "tweet":
            self.__stop_twiter_service()
        else:
            self.__logger.error("Unsupported service")

    async def __start(self) -> None:
        if not self.config:
            self.start_service("email")
            self.start_service("rss")
            self.start_service("tweet")
        else:
            for key, value in self.config.SERVICES.items():
                if value:
                    self.start_service(key)
        if not self.__rss_service:
            return
        while True:
            entry: RSSService.ParsedEntry = await self.__rss_service.interact()
            if self.__email_service:
                self.__email_service.interact(entry["summary_detail"])
            elif self.__tweet_service:
                self.__tweet_service.interact(TweetObject(
                    entry["summary_detail"], entry["link"]))
            sleep(10)

    def start(self):
        asyncio.run(self.__start())

    def stop(self):
        try:
            self.__stop_twiter_service();
        except: ...
        try: 
            self.__stop_email_service();
        except: ...
        try: 
            self.__stop_rss_service()
        except: ...

if __name__ == '__main__':
    bot: Bot = Bot()
    bot.start()
    try:
        while True: ...
    except KeyboardInterrupt:
        bot.stop_service("email")
        bot.stop_service("rss")
        bot.stop_service("tweet")