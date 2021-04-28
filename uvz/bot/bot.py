import os
from django import db
import requests
from dotenv import load_dotenv
from uvz.email.EmailClient import EmailClient
from uvz.utilities.decorators import raiseAndJSON
from uvz.models.emailAddresses import EmailAddresses
from typing import Any, Dict, List, Optional, TypedDict, Union

load_dotenv()
BASE_URl = os.environ.get("BASE_URL")


class RecordRespose(TypedDict):
    published: str
    link: str
    description: str
    title: str


@raiseAndJSON
def get_last_record(token: str) -> Union[Any, RecordRespose]:
    return requests.post(f"{BASE_URl}/api/rss/lastRecord", json={
        "token": token
    })


@raiseAndJSON
def put_to_db(payload=None, token=None) -> Union[Any, RecordRespose]:
    return requests.put(f"{BASE_URl}/api/database/insertRecord/", json={
        "token": token,
        "record": payload
    })


@raiseAndJSON
def make_tweet(payload=None, token=None) -> Union[Any, RecordRespose]:
    payload["description"] = payload["description"].replace(
        '\"', "\'")
    return requests.post(f"{BASE_URl}/api/twitter/makeTweet", json={
        "token": token,
        "record": payload
    })


@raiseAndJSON
def send_mails(payload: Dict[str, Any] = {
    "token": "token",
    "emailMessage": "<h1>Test message</h1>",
    "recievers": [
        "mtoth575@gmail.com"
    ],
    "is_html": True
}):
    return requests.post(f"{BASE_URl}/api/email/sendMail", json=payload)


@raiseAndJSON
def get_records_from_db(token, ammount: int = 10) -> Union[List[Union[Any, RecordRespose]], Any]:
    return requests.post(f"{BASE_URl}/api/database/readRecords/", json={
        "token": token,
        "pageSize": ammount
    })


@raiseAndJSON
def get_auth_token(username: Optional[str] = os.environ["PERSONAL_MAIL"], password: Optional[str] = os.environ["PERSONAL_EMAIL_PASSWORD"]):
    return requests.post(f"{BASE_URl}/api/auth/getToken/", json={
        "username": username,
        "password": password
    })


def pop_key_from_list(old_dict):
    new_dict = old_dict.copy()
    new_dict.pop('id', None)
    new_dict.pop('link', None)
    new_dict.pop('published', None)
    return new_dict


def ammend_record(*records):
    if len(records) == 1:
        return next(map(pop_key_from_list, records))
    return tuple(map(pop_key_from_list, records))


def is_new_record(token):
    records = get_records_from_db(token)
    db_record = get_last_record(token)
    if ammend_record(db_record) in ammend_record(*records):
        return
    return db_record


def get_emails():
    return EmailAddresses.objects.values_list('email', flat=True)


def bot_run():
    print(f"<{'-'*80}>")
    token = get_auth_token().get("token")
    if (record := is_new_record(token)):
        put_to_db(payload=record, token=token)
        make_tweet(payload=record, token=token)
        with EmailClient() as client:
            client.send_mail(record["description"],
                             *get_emails(), is_html=True)
        print(f"{'#'*20}New Record{'#'*20}")
