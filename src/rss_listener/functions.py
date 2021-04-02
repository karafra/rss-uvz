import smtplib
from os import environ
from src.tweet_api.functions import make_tweet
import feedparser as fp
from datetime import datetime
from time import sleep, mktime, struct_time
from email.mime.text import MIMEText
from feedparser.util import FeedParserDict
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage, Message
from typing import Any, Dict, List, Optional, Tuple, TypedDict, Union


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


def start_SMTP(address: str, password: str, retries: int = 5) -> Optional[smtplib.SMTP]:
    """
    Logs into existing SMTP server with 'email' and 'password' credentials.
    :param address: email address of user on smtp server
    :type address: str
    :param password: passsword on user on server
    :type password: str
    :param retries: number of retires to do after error
    :type retries: int

    :return: smtplib.SMTP | None  
    """
    try:
        session: smtplib.SMTP = smtplib.SMTP("smtp.gmail.com", 587)
        session.ehlo()
        session.starttls()
        session.login(address, password)
        return session
    except smtplib.SMTPAuthenticationError as err:
        if retries > 0:
            start_SMTP(address, password, retries - 1)
        else:
            print(f"[ERROR]: {str(err)}")


def send_mail(smtp_session: smtplib.SMTP, reciever: str, email: EmailMessage) -> None:
    """
    Takes initialized SMTP server session, and sends email from it to recievers.

    :param smtp_session: smtp server session
    :type smtp_session: smtplib.SMTP
    :param reciever: Recievers of email
    :type reciever: str
    :param email: Fully sanitized EmailMessge object
    :type email: email.message.EmailMessage

    :return: None
    """
    sign_up_email: str = f"{reciever.split('@')[0]}+uvz_update@{reciever.split('@')[1]}"
    smtp_session.sendmail(
        "admin@admin.com", sign_up_email, msg=email.as_string())


def body_with_link(body: str, link: str) -> MIMEText:
    """
    Builds HTMl email cosisting of body and link to more information.

    :param body: main part of email
    :type body: str 
    :param link: link to more information
    :type lin: str

    :returns: MIMEText
    """
    return MIMEText(f"""
    <html>
      <head></head>
        <body>
            {body}
            <br />
            <p>
                <a href={link}> Full article </a>
            </p>
        </body>
    </html>
    """, "html")


def html_email_body(body: str) -> MIMEText:
    """
    Builds simple HTML email.

    :param body: body of email
    :type body: str

    :return: MIMEText
    """
    return MIMEText(f"""
    <html>
      <head></head>
        <body>
            {body}
        </body>
    </html>
    """, "html")


def send_covid_update(text: str, recievers: Union[List[str], Tuple[str, ...], str], link: str = None) -> None:
    """
    Sends covid update from UVZ to list of recievers.
    Reciever mails are amended.
        Example: admin@admin.com --> admin+uvz_update@admin.com
    Email msg format is such as:
        SUBJECT: ÚVZ update from YYYY-MM-DD hh:mm:ss:ms[6]
        BODY: 
            V 13. kalendárnom týždni 2021 bolo hlásených 5 723 akútnych respiračných ochorení (ARO), t. j. chorobnosť 328,0/100 000 osôb v starostlivosti lekárov hlásiacich v tomto kalendárnom týždni. Chorobnosť v porovnaní s predchádzajúcim týždňom klesla o 24,3 % (graf 1). Najvyššia chorobnosť bola zaznamenaná v Košickom kraji, najnižšia v Banskobystrickom kraji. Najvyššia vekovo špecifická chorobnosť na ARO bola vo vekovej skupine 0 – 5 ročných detí, dosiahla hodnotu 955,3/100 000 (graf 2).
            LINK: Full article. 

    :param text: text of email
    :type text: str
    :param recievers: list of recievers
    :type recievers: Union[List[str], Tuple[str, ...]
    :param link: link to full article
    :type link: str
    """

    sesion: Optional[smtplib.SMTP] = start_SMTP(
        "mtoth575+uvz_updates@gmail.com", "dedomraz49")
    if not sesion:
        return
    msg: Message = MIMEMultipart("alternative")
    msg['Subject'] = f"ÚVZ update from {datetime.now()}"
    if link:
        msg.attach(body_with_link(text, link=link))
    else:
        msg.attach(html_email_body(text))
    if isinstance(recievers, str):
        sesion.sendmail("test@gmail.com", recievers, msg.as_string())
        print(f"[INFO]: Update to {recievers} sent!")
        sesion.close()
        return
    for email_address in recievers:
        try:
            sesion.sendmail("test@gmail.com", email_address, msg.as_string())
            print(f"[INFO]: Update to {email_address} sent!")
        except Exception as err:
            print(f"[ERROR]: {str(err)}")
    sesion.close()


def listen_for_updates() -> None:
    """
    Listens for updates in rss feed. When the feed updated, sends mail to 
    all users specified in 'recievers' environment variable. Feed
    is refreshed every 10 seconds.

    :returns: None
    """
    LAST_PUBLISHED = datetime.now()
    while True:
        sleep(10)
        rss_feed = load_entries()
        last_entry = rss_feed[0]
        if datetime.fromtimestamp(mktime(last_entry["published_parsed"])) < LAST_PUBLISHED:
            listen_for_updates()
        recievers: List[str] = environ["reciever_emails"].split(";")
        send_covid_update(
            last_entry["summary_detail"], recievers=recievers, link=last_entry["link"])
        make_tweet(last_entry["summary_detail"], last_entry["link"])
        LAST_PUBLISHED = datetime.now()
        print("\033[92m[INFO]: New record found!\033[92m")
        listen_for_updates()
