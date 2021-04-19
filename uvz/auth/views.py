from uvz.utilities.decorators import validateTokenInBody, validate_post_request_body
import jwt
import json
from time import time
from django.contrib import auth
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from os import environ

@require_POST
@validate_post_request_body({
    "username": "Username of user to authorize",
    "password": "Password of user to authroize"
})
def get_token(request: HttpRequest):
    request_dict = json.loads(request.body.decode("utf-8"))
    if user := authenticate(
        username=request_dict["username"],
        password=request_dict["password"]):
        return JsonResponse({
            "token": jwt.encode({
                "iss": "uvz-rss.auth",
                "sub": user.get_username(),
                "iat": (time_ := time()),
                "exp": (time_ + 300),
                "loggedInAs": user.get_username(),
            }, key=environ["PRIVATE_KEY_JWT"], algorithm="HS256")
        })
    return JsonResponse({
        "Error": "Username nad password do not match, or user with theese credentials does not exist"
    })

@require_POST
@validate_post_request_body({
    "token": "Token to validate"
})
def validate_token(request: HttpRequest):
    request_dict = json.loads(request.body.decode("utf-8"))
    try:
        token = jwt.decode(request_dict["token"], key=environ["PRIVATE_KEY_JWT"], algorithms="HS256")
        return JsonResponse({
            "isValid": True, 
            "tokenDecoded": token
        })
    except jwt.ExpiredSignatureError:
        return JsonResponse({
            "isValid": False,
            "Error": "Token expired"
        })
    except jwt.InvalidTokenError:
        return JsonResponse({
            "isValid": False,
            "Error": "Token is not not in correct format"
        })
    except Exception as err:
        return JsonResponse({
            "isValid": False,
            "Error": str(err)
        })