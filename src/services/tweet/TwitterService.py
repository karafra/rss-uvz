import tweepy
import logging
from tweepy import api
from os import environ
from tweepy.api import API
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from src import IService, AbstractProcess
from typing import Optional, Any, Callable


class TwitterConfig(object):
    def __init__(self, api_key: str, api_key_secret: str, access_token: str, access_token_secret: str) -> None:
        self.api_key = api_key
        self.api_key_secret = api_key_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        super().__init__()


class TweetObject(object):
    def __init__(self, text, link) -> None:
        self.text = text
        self.link = link
        super().__init__()


class TwitterService(IService):

    class _TWITTER_PROCESS(AbstractProcess):

        @staticmethod
        def init_api(config: TwitterConfig) -> Optional[API]:
            """
            Initializes twiter config object, this also function verifies if tokens are corect.
            """
            auth = tweepy.OAuthHandler(config.api_key, config.api_key_secret)
            auth.set_access_token(config.access_token,
                                  config.access_token_secret)
            api = tweepy.API(auth)
            try:
                api.verify_credentials()
                return api
            except Exception as err:
                logging.error(str(err))
                raise err

        def get_short_link(self, link: str) -> str:
            """
            Returns url address shortened by twiter url shortner.

            :param link: link to shorten
            :type link: str

            :return: str
            """
            response = self.api.update_status(link)
            # For some fucking reason VScode decided that this code will throw error ...
            self.api.destroy_status(id=response.id_str) # pylint: disable=cannot-access-member
            # Same as above, I have no idea why ...
            return response.text

        def make_tweet(self, text: str, link: str) -> None:
            """
            Function that make twwet with appropirate length, 
            and adds link if some are present.
            This function also post this tweet to twiter.

            :param text: text of tweet
            :type text: str
            :param link: link to be added to tweet
            :type link: str

            :return: None 
            """
            soup: BeautifulSoup = BeautifulSoup(text, features="lxml")
            tweet: str = ""
            link = self.get_short_link(link)
            text = TwitterService._shorten_tweet(
                soup.get_text(), offset=len(link))
            tweet = f"{text}\n\n{link}"
            api.update_status(tweet)
            logging.info("Tweet published ({tweet or text})")

        def __init__(self, target: Callable[..., Any], twiter_config: TwitterConfig):
            self.api: Optional[API] = self.init_api(twiter_config)
            super().__init__(target)

        def _thread_function(self) -> None:
            while True:
                obj: TweetObject = self.args_queue.get()
                self.make_tweet(obj.text, obj.link)

    def __load_environmnet_variables(self) -> TwitterConfig:
        try:
            return TwitterConfig(
                environ["API_KEY"],
                environ["API_KEY_SECRET"],
                environ["ACCESS_TOKEN"],
                environ["ACCESS_TOKEN_SECRET"]
            )
        except Exception as err:
            logging.error("Missing envirnment varibles, required environmnet variables are: \n\t\
                    - API_KEY: api key to Twitter api \n\t\
                    - API_KEY_SECRET: api kez secret to twitter api\n\t\
                    - ACCESS_TOKEN: access token to Twitter api (needs to be generated separately) \n\t\
                    - ACCESS_TOKEN_SECRET: access token secret to Twitter api (needs to be generated separately)")
            raise err

    def __init__(self) -> None:
        load_dotenv()
        self.twitter_config: TwitterConfig = self.__load_environmnet_variables()
        super().__init__()

    @staticmethod
    def _shorten_tweet(text: str, offset: int = 0) -> str:
        """
        Shorten tweet if its longer than 280 characters.

        :param text: text of tweet
        :type text: str
        :param offset: length of aditional texts in tweet
        :type offset: int

        :return: str
        """
        if len(text) < (280 - 6 - offset):
            return text + " ..."
        return TwitterService._shorten_tweet(" ".join((text.split(" ")[:-1])), offset=offset)

    def start_service(self):
        self.process = self._TWITTER_PROCESS(
            self._shorten_tweet, self.twitter_config)

    def stop_service(self):
        self.process._stop()


if __name__ == "__main__":
    #Code for quick tesing 
    service: TwitterService = TwitterService()
    service.start_service()
    while True:
        pass
