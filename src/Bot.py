import asyncio
import logging
from os import environ
from time import sleep
from dotenv import load_dotenv
from src.IService import IService
from typing import Literal, Optional
from src.services.rss.RSSService import RSSService
from src.services.email.EmailService import EmailService
from src.services.tweet.TwitterService import TweetObject, TwitterService


class Bot(object):

    def __init__(self) -> None:
        load_dotenv()
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

    def start_service(self, service: Literal["email", "rss", "tweet"]) -> None:
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

    def stop_service(self, service: Literal["email", "rss", "tweet"]) -> None:
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
        self.start_service("email")
        self.start_service("rss")
        #self.start_service("tweet")
        while True:
            entry: RSSService.ParsedEntry = await self.__rss_service.interact()
            self.__email_service.interact(entry["summary_detail"])
         #   self.__tweet_service.make_tweet(TweetObject(
         #       entry["summary_detail"], entry["link"]))
            sleep(10)

    def start(self):
        asyncio.run(self.__start())


if __name__ == '__main__':
    bot: Bot = Bot()
    bot.start_service("rss")
