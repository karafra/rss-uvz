import json
import requests
from requests import Response
from typing import Any, Dict, Union
from django.http.request import HttpRequest
from django.http.response import JsonResponse


def delete_optional(sample_body):
    for key, value in sample_body.copy().items():
        if "(optional)" in str(value):
            del sample_body[key]
    return sample_body


def validate_request_body(sample_body: Union[Dict[str, str], Dict[str, Dict[str, str]]] = {"token": "Authentification token", }, status_if_failed: int = 400):
    def _validate_post_request_body(func):
        def __validate_post_request_body(request: HttpRequest, *args, **kwargs):
            sample_body = delete_optional(json.loads(request.body))
            if set(sample_body).issubset(set(json.loads(request.body.decode("utf-8")))):
                return func(request, *args, **kwargs)
            err_dict: Dict[str, str] = {
                "Error": f"Missing value, request has to be subset of this dict {sample_body}"}
            return JsonResponse(err_dict, status=status_if_failed)
        return __validate_post_request_body
    return _validate_post_request_body


def raiseAndJSON(func):
    def _raiseAndJSON(*args, **kwargs) -> Dict[str, Any]:
        response: Response = func(*args, **kwargs)
        try:
            response.raise_for_status()
        except Exception as e:
            raise Exception(str(e)) from e
        return response.json()
    return _raiseAndJSON


def validate_token_in_body(func):
    def _validateTokenInBody(*args, **kwargs):
        request: HttpRequest = args[0]
        request_dict = json.loads(request.body.decode("utf-8"))
        if not ((token := request_dict.get("token")) or (token := request.COOKIES.get("token"))):
            return JsonResponse({
                "Error": "Auth token is missing"
            })
        response = requests.post(f"http://{request.META['HTTP_HOST']}/api/auth/validateToken/", json={
            "token": token
        })
        try:
            response.raise_for_status()
            if "Error" in (response_json := response.json()) or "error" in response_json:
                raise Exception(
                    f"Error: {response_json.get('error') or response_json.get('Error')}")
        except Exception as err:
            return JsonResponse({
                "Error": f"Token is not valid ({str(err)})"
            })
        return func(*args, **kwargs)
    return _validateTokenInBody
