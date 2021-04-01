import os
from flask import render_template
import smtplib
from os import environ
import feedparser as fp
from flask import Flask
from datetime import datetime
from datetime import datetime
from time import mktime, sleep
from email.mime.text import MIMEText
from feedparser.util import FeedParserDict
from email.mime.multipart import MIMEMultipart
from typing import List, Optional, Tuple, Union
from email.message import EmailMessage, Message
from flask_apscheduler import APScheduler, scheduler


def load_entries():
    feed: FeedParserDict = fp.parse(
        "https://www.uvzsr.sk/index.php?option=com_content&view=frontpage&Itemid=1&type=atom&format=feed"
    )
    out_dict = []
    for record in feed["entries"]:
        out_dict.append({
            "title": record["title"],
            "link": record["link"],
            "published_parsed": record["published_parsed"],
            "summary_detail": record["summary"]
        })
    return out_dict


def start_SMTP(address: str, password: str, retries=5):
    try:
        session = smtplib.SMTP("smtp.gmail.com", 587)
        session.ehlo()
        session.starttls()
        session.login(address, password)
        return session
    except smtplib.SMTPAuthenticationError as err:
        if retries > 0:
            start_SMTP(address, password, retries - 1)
        else:
            print(f"[ERROR]: {str(err)}")


def send_mail(smtp_session: smtplib.SMTP, reciever: str, email: EmailMessage):
    sign_up_email: str = f"{reciever.split('@')[0]}+uvz_update@{reciever.split('@')[1]}"
    smtp_session.sendmail(
        "admin@admin.com", f"{sign_up_email}", msg=email.as_string())


def body_with_link(body, link): return MIMEText(f"""
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


def html_email_body(body): return MIMEText(f"""
    <html>
      <head></head>
        <body>
            {body}
        </body>
    </html>
    """, "html")


def send_covid_update(text: str, recievers: Union[List[str], Tuple[str], str], link=None):
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


def listen_for_updates():
    LAST_PUBLISHED = datetime.now()
    while True:
        sleep(10)
        rss_feed = load_entries()
        last_entry = rss_feed[0]
        if datetime.fromtimestamp(mktime(last_entry["published_parsed"])) < LAST_PUBLISHED:
            print("[INFO]: No new records!")
            listen_for_updates()
        recievers: List[str] = environ["reciever_emails"].split(";")
        send_covid_update(
            last_entry["summary_detail"], recievers=recievers, link=last_entry["link"])
        LAST_PUBLISHED = datetime.now()
        listen_for_updates()


class FlaskConfig(object):
    JOBS = [
        {
            "id": "listen_for_updates",
            "func": "app:listen_for_updates",
        }
    ]


app: Flask = Flask(__name__)
app.config.from_object(FlaskConfig)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def default(path):
    full_path = os.path.join("static", "images", "ouroboros.gif")
    return render_template("ouroboros.html", user_image=full_path)

if __name__ == '__main__':
    app.run()
