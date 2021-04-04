from email.mime import text
import logging
import smtplib
from os import environ, link
from typing import List, Optional
from datetime import datetime
from dotenv import load_dotenv
from src.IService import IService
from email.message import Message
from abc import ABC, abstractmethod
from email.mime.text import MIMEText
from typing import Union, Callable, Any
from email.mime.multipart import MIMEMultipart
from src.AbstractProcess import AbstractProcess


class EmailService(IService):
    """
    Service for sendng emails with RÚVZ updates.
    This service supports HTML markdown, 
    and is running as paralllel process.
    """
    STMP_PORT: int = 587
    SMTP_URL: str = "smtp.gmail.com"

    class _EmailObj(object):
        def __init__(self, text: str, link: Optional[str]) -> None:
            self.text: str = text
            self.link: Optional[str] = link
            super().__init__()

    class _PROCESS(AbstractProcess):

        def __init__(self, address: str, password: str, target: Optional[Union[Callable[..., Any]]] = None):
            self.address: str = address
            self.password: str = password
            self.recipients: str = self.__check_environment_variables()
            self.smtp_session: Optional[smtplib.SMTP] = None
            super().__init__(target=self._thread_function)

        def __send_mail(self, reciever: str, email: Message) -> None:
            """
            Takes sends email from smtp_session to recievers.

            :param reciever: Recievers of email
            :type reciever: str
            :param email: Fully sanitized EmailMessge object
            :type email: email.message.EmailMessage

            :return: None
            """
            sign_up_email: str = f"{reciever.split('@')[0]}+uvz_update@{reciever.split('@')[1]}"
            self.smtp_session.sendmail(
                "admin@admin.com", sign_up_email, msg=email.as_string())

        def __start_SMTP(self, retries) -> Optional[smtplib.SMTP]:
            """
            Logs into existing SMTP server with 'email' and 'password' credentials.
            :param retries: number of retires to do after error
            :type retries: int

            :return: smtplib.SMTP | None  
            """
            try:
                session: smtplib.SMTP = smtplib.SMTP(
                    EmailService.SMTP_URL, EmailService.STMP_PORT)
                session.ehlo()
                session.starttls()
                session.login(self.address, self.password)
                return session
            except smtplib.SMTPAuthenticationError as err:
                if retries > 0:
                    self.__start_SMTP(retries - 1)
                else:
                    raise err

        def _thread_function(self) -> None:
            while True:
                if not self.smtp_session:
                    self.smtp_session = self.__start_SMTP(5)
                msg: Message = self.__build_email(self.args_queue.get())
                if isinstance(self.recipients, str):
                    self.__send_mail(self.recipients, msg)
                    continue
                for recipient in self.recipients or []:
                    self.__send_mail(recipient, msg)

        @staticmethod
        def __check_environment_variables() -> str:
            """
            Checks if all envirnment variables are present.
            Required environment variables:
                - reciever_emails: recipents of updates
            :returns: str
            """
            try:
                return environ["reciever_emails"]
            except Exception as err:
                print(
                    "[ERROR]: Missing environmnet variables\nRequired environment variables: reciever_emails")
                raise err

        @staticmethod
        def __email_with_html_body_and_link(body: str, link: str) -> MIMEText:
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

        @staticmethod
        def __email_with_html_body(body: str) -> MIMEText:
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

        def __build_email(self, email_obj: "EmailService._EmailObj") -> Message:
            """
            Builds covid update email in html form.

            :param text: text in the body of email
            :type text: str
            :param link: optional link to more site that contains more information
            :type link: str

            :returns: Message
            """
            msg: Message = MIMEMultipart("alternative")
            msg['Subject'] = f"ÚVZ update from {datetime.now()}"
            if email_obj.link:
                msg.attach(self.__email_with_html_body_and_link(
                    email_obj.text, link=email_obj.link))
            else:
                msg.attach(self.__email_with_html_body(email_obj.text))
            return msg

    def __init__(self, address: str, password: str) -> None:
        load_dotenv()
        self.address: str = address
        self.password: str = password
        self.session: Optional[smtplib.SMTP] = None
        self.process = None
        super().__init__()

    def interact(self, text: str, link: Optional[str] = None) -> None:
        obj: "EmailService._EmailObj" = self._EmailObj(text, link or None)
        self.process.args_queue.put(obj)

    def start_service(self) -> None:
        """Start email service, as new process."""
        if not self.process:
            self.process = self._PROCESS(
                address=self.address, password=self.password)

    def stop_service(self) -> None:
        """Stop email service, and coresponding process."""
        self.process._stop()


if __name__ == "__main__":
    # Code for quick testing
    emailService: EmailService = EmailService(
        environ["PERSONAL_MAIL"], environ["PERSONAL_MAIL_PASSWORD"])
    emailService.start_service()
    while True:
        input_ = input("Payload: ")
        if input_ == "stop":
            emailService.stop_service()
            break
        emailService.interact(input_)
