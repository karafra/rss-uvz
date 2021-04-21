from typing import Any, Dict, List, Optional, TypedDict, Union
from uvz.utilities.decorators import raiseAndJSON
import requests
import os
from dotenv import load_dotenv

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
    return requests.put(f"{BASE_URl}/api/database/insertRecord", json={
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
def get_record_from_db(token, ammount: int = 10) -> Union[List[Union[Any, RecordRespose]], Any]:
    return requests.post(f"{BASE_URl}/api/database/readRecords", json={
        "token": token,
        "pageSize": ammount
    })


@raiseAndJSON
def get_auth_token(username: Optional[str] = os.environ["reciever_emails"], password: Optional[str] = os.environ["password"]):
    return requests.post(f"{BASE_URl}/api/auth/getToken", json={
        "username": username,
        "password": password
    })


def pop_key_from_list(old_dict):
    new_dict = old_dict.copy()
    new_dict.pop('id', None)
    return new_dict


def is_new_record(token):
    if (response := get_last_record(token)) in tuple(map(pop_key_from_list, get_record_from_db(token))):
        return
    return response


def bot_run():
    print(f"<{'-'*80}>")
    token = get_auth_token().get("token")
    if (record := is_new_record(token)):
        put_to_db(payload=record, token=token)
        make_tweet(payload=record, token=token)
        print(f"{'#'*20}New Record{'#'*20}")
