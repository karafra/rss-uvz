import json
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from uvz.utilities.decorators import validate_request_body
from uvz.auth.functions import generate_auth_token, validate_auth_token


@require_POST
@validate_request_body({
    "username": "Username of user to authorize",
    "password": "Password of user to authroize"
})
def get_token(request: HttpRequest):
    request_dict = json.loads(request.body.decode("utf-8"))
    if token := generate_auth_token(request_dict["username"], request_dict["password"], expiration=600):
        refresh_token = generate_auth_token(
            request_dict["username"], request_dict["password"], expiration=3600*2)
        return JsonResponse({
            "token": token,
            "refreshToken": refresh_token
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
    return JsonResponse(validate_auth_token(request_dict.get("token")))


@require_POST
@validate_request_body(sample_body={
    "refreshToken": "Token used to authorize refresh of token (optional)"
})
def refresh_token(request: HttpRequest):
    token = json.loads(request.body.decode("utf-8")).get("refreshToken") or request.COOKIES.get("refreshToken")
    response = validate_auth_token(token)
    if not response.get("isValid"):
        return JsonResponse(response)
    username = response.get("tokenDecoded").get("sub")
    response = JsonResponse({
            "token": (token := generate_auth_token(None, None, username_=username, expiration=600)),
            "refreshToken": (refresh_token := generate_auth_token(None, None, username_=username, expiration=3600*2))
        })
    response.set_cookie("token", token, httponly=True)
    response.set_cookie("refreshToken", refresh_token, httponly=True)
    return response 
