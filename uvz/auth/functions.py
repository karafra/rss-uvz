from django.views.decorators.http import last_modified
import jwt
from time import time
from os import environ
from dotenv import load_dotenv
from django.contrib.auth import authenticate

load_dotenv()

def generate_auth_token(username, password):
    user = authenticate(    
        username=username,
        password=password)
    if not user:
        return ""    
    return str(jwt.encode({
            "iss": "uvz-rss.auth",
                "sub": user.get_username(),
                "iat": (time_ := time()),
                "exp": (time_ + 300),
                "loggedInAs": user.get_username(),
            }, key=environ["PRIVATE_KEY_JWT"], algorithm="HS256"))
    
