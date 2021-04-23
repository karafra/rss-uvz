import tweepy
from os import environ
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from uvz.rss.views import ParsedEntry


class TwitterApi(tweepy.API):
    
    def __init__(self, *args, **kwargs):
        load_dotenv()
        auth_handler = tweepy.OAuthHandler(
            environ["API_KEY"],
            environ["API_KEY_SECRET"],
        )
        auth_handler.set_access_token(
            environ["ACCESS_TOKEN"],
            environ["ACCESS_TOKEN_SECRET"],
        )
        super().__init__(auth_handler=auth_handler, *args, **kwargs)

    @staticmethod
    def __shorten_tweet(text: str, offset: int = 0) -> str:
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
        return TwitterApi.__shorten_tweet(" ".join((text.split(" ")[:-1])), offset=offset)


    def __get_short_link(self, link: str) -> str:
        """
        Returns url address shortened by Twiter url shortner
        :param link: link to shorten
        :type link: st
        :return: str
        """
        response = super().update_status(link)
        # For some fucking reason VScode decided that this code will throw error ...
        self.destroy_status(
            id=response.id_str)  # type: ignore
        # Same as above, I have no idea why ...
        return response.text     # type: ignore

    def update_status(self, rss_tweet: ParsedEntry=None, *args, **kwargs):
        link = self.__get_short_link(rss_tweet.link)
        soup: BeautifulSoup = BeautifulSoup(rss_tweet.description)
        tweet: str = f"{TwitterApi.__shorten_tweet(soup.get_text(), offset=len(link))}\n\n{link}"
        return super().update_status(tweet, *args, **kwargs)
