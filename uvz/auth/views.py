from uvz.auth.functions import generate_auth_token
from uvz.utilities.decorators import validate_token_in_body, validate_request_body
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
@validate_request_body({
    "username": "Username of user to authorize",
    "password": "Password of user to authroize"
})
def get_token(request: HttpRequest):
    request_dict = json.loads(request.body.decode("utf-8"))
    if token := generate_auth_token(request_dict["username"], request_dict["password"]):
        return JsonResponse({
            "token": token
        })
    return JsonResponse({
        "Error": "Username nad password do not match, or user with theese credentials does not exist"
    })


@require_POST
@validate_request_body({
    "token": "Token to validate (optional)"
})
def validate_token(request: HttpRequest):
    request_dict = json.loads(request.body.decode("utf-8"))
    try:
        token = jwt.decode(
            request_dict["token"], key=environ["PRIVATE_KEY_JWT"], algorithms="HS256")
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
