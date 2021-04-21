import json
from logging import error
from requests import Response
from typing import Any, Dict, Union
from django.http.request import HttpRequest
from django.http.response import JsonResponse
import requests

def validate_request_body(sample_body: Union[Dict[str, str], Dict[str, Dict[str, str]]]  = {"token": "Authentification token", }, status_if_failed: int = 400):
    def _validate_post_request_body(func):
        def __validate_post_request_body(request: HttpRequest, *args, **kwargs):
            if set(sample_body).issubset(set(json.loads(request.body.decode("utf-8")))):
                return func(request, *args, **kwargs)
            err_dict: Dict[str, str] = {
                "Error": f"Missing value, request has to be subset of this dict {sample_body}"}
            return JsonResponse(err_dict, status=status_if_failed)
        return __validate_post_request_body
    return _validate_post_request_body


def raiseAndJSON(func):
    def _raiseAndJSON(*args, **kwargs) -> Any:
        response: Response = func(*args, **kwargs)
        try:
            response.raise_for_status()
        except Exception as e:
            print(response.json())
            raise Exception(str(e)) from e
        return response.json()
    return _raiseAndJSON


def validate_token_in_body(func):
    def _validateTokenInBody(*args, **kwargs):
        request_dict = json.loads(args[0].body.decode("utf-8"))
        token = request_dict["token"]
        response = requests.post(f"http://{args[0].META['HTTP_HOST']}/api/auth/validateToken", json={
            "token": token
        })
        try: 
            response.raise_for_status()
            if "Error" in (response_json := response.json()) or "error" in (response_json := response.json()):
                raise Exception(f"Error: {response_json.get('error') or response_json.get('Error')}")
        except Exception as err:
            return JsonResponse({
                "Error": f"Token is not valid ({str(err)})"
            })
        return func(*args, **kwargs)
    return _validateTokenInBody
