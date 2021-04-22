from django.contrib.auth.models import User
from django.views.decorators.http import last_modified
import jwt
from time import time
from os import environ
from dotenv import load_dotenv
from django.contrib.auth import authenticate

load_dotenv()


def generate_auth_token(username, password, expiration=300, username_=None):
    if not (username_ or  (user := authenticate(
            username=username,
            password=password))):
        return ""
    return str(jwt.encode({
        "iss": "uvz-rss.auth",
        "sub": username_ or user.get_username(), # type: ignore
        "iat": (time_ := time()),
        "exp": (time_ + expiration),
        "loggedInAs": username_ or user.get_username(), # type: ignore
    }, key=environ["PRIVATE_KEY_JWT"], algorithm="HS256"))


def validate_auth_token(token):
    try:
        token = jwt.decode(
            token, key=environ["PRIVATE_KEY_JWT"], algorithms="HS256")
        return {
            "isValid": True,
            "tokenDecoded": token
        }
    except jwt.ExpiredSignatureError:
        return {
            "isValid": False,
            "Error": "Token expired"
        }
    except jwt.InvalidTokenError:
        return {
            "isValid": False,
            "Error": "Token is not not in correct format"
        }
    except Exception as err:
        return {
            "isValid": False,
            "Error": str(err)
        }
