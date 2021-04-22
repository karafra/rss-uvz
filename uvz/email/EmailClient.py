import ssl
import smtplib
import sys
from os import environ
from datetime import datetime
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

class EmailClient(object):
    __PORT = 465
    __APP_PASSWORD = environ["EMAIL_APP_PASSWORD"]
    __CONTEXT = ssl.create_default_context()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.kill_server()

    def __init__(self) -> None:
        self.__server = smtplib.SMTP_SSL(
            "smtp.gmail.com", self.__PORT, context=self.__CONTEXT)
        self.__server.ehlo()
        self.__server.login("mtoth575@gmail.com", self.__APP_PASSWORD)
        self.__server.ehlo()

    def kill_server(self):
        self.__server.close()

    def send_mail(self, text: str, *recievers, is_html=False):
        msg: MIMEMultipart = MIMEMultipart("alternative")
        msg["Subject"] = f"ÚVZ update from {datetime.now()}"
        msg["From"] = "mtoth575@gmail.com"
        if is_html:
            msg.attach(MIMEText(text, "html"))
        else:
            msg.attach(MIMEText(text, "plain"))
        for reciever in recievers:
            msg["To"] = reciever
            try:
                self.__server.sendmail("mtoth575@gmail.com",
                                    reciever, msg.as_string())
            except Exception as err:
                print(str(err), file=sys.stderr)