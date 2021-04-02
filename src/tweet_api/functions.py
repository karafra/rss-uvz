from typing import Optional, List, TypedDict, Any
import tweepy
from time import struct_time
import feedparser as fp
from feedparser import FeedParserDict
from os import environ
from dotenv import load_dotenv
from tweepy.api import API
from bs4 import BeautifulSoup

load_dotenv()

def init_api() -> Optional[API]:
    """
    Initializes twiter api from env varibles, also this function verifies if tokens are corect.
    Required environmnet variables:
        API_KEY: Your api key
        API_SECRET: Your api secret
        ACCESS_TOKEN: Your access token. Has to be generated separately
        ACCESS_SECRET: Your access secret. Has to be generated separately

            
    """
    auth = tweepy.OAuthHandler(environ["API_KEY"], environ["API_SECRET"])
    auth.set_access_token(environ["ACCESS_TOKEN"], environ["ACCESS_SECRET"])
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        return api
    except Exception as e:
        print(f"[ERROR]: {str(e)}")

def contains_link(text: str) -> Optional[str]:
    """
    Check if text contains link stored in <a> tag, 
    if so function returns this link.

    :param text: text to search for link
    :type text: str
    :return: str | None
    """
    soup: BeautifulSoup = BeautifulSoup(text, features="lxml")
    #Check if anchor tag is present
    if not soup.find("a"):
        return
    try:
        return soup.find("a")["href"]
    except:
        return

def shorten_tweet(text: str, offset: int=0) -> str:
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
    return shorten_tweet(" ".join((text.split(" ")[:-1])), offset=offset)

def get_short_link(link: str) -> str:
    """
    Returns url address shortened by twiter url shortner.

    :param link: link to shorten
    :type link: str

    :return: str
    """
    api: Optional[API] = init_api()
    if not api:
        return "";
    response = api.update_status(link)
    # For some fucking reason VScode decided that this code will throw error ...
    api.destroy_status(id=response.id_str)
    return response.text

def make_tweet(text: str, link:str=None) -> None:
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
    api: Optional[API] = init_api()
    if not api:
        return
    soup: BeautifulSoup = BeautifulSoup(text, features="lxml")
    tweet: str = ""
    #Check for links hidden in achor tags
    if anchor_link := contains_link(text):
        anchor_link = get_short_link(anchor_link)
        text = shorten_tweet(soup.get_text(), offset=len(anchor_link))
        tweet: str = f"{text}\n\n{anchor_link}"    
    if link and not link.endswith((".pdf", ".xlxs")):
        link = get_short_link(link)
        text = shorten_tweet(soup.get_text(), offset=len(link))
        tweet: str = f"{text}\n\n{link}"
    if not tweet:
        api.update_status(shorten_tweet(soup.get_text()))
        return
    api.update_status(tweet)
    print(f"[INFO]: Tweet published ({tweet or text})")

class ParsedEntry(TypedDict):
    title: str
    link: str
    published_parsed: struct_time
    summary_detail:  str


def load_entries() -> List[ParsedEntry]:
    """
    Function that loads rss entries from Úrad verejného zdravotníctva.
    This function also parses out the unnecessary parts of RSS records
    such as detailed descriptions, names of authors and/or time when it was updated.
    """
    feed: FeedParserDict = fp.parse(
        "https://www.uvzsr.sk/index.php?option=com_content&view=frontpage&Itemid=1&type=atom&format=feed"
    )
    out_dict: List[Any] = []
    for record in feed["entries"]:
        out_dict.append({
            "title": record["title"],
            "link": record["link"],
            "published_parsed": record["published_parsed"],
            "summary_detail": record["summary"]
        })
    return out_dict

