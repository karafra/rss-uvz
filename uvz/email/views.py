
import json
from uvz.utilities.decorators import validateTokenInBody
from uvz.email.EmailClient import EmailClient
from django.views.decorators.http import require_POST
from uvz.utilities.decorators import validate_post_request_body
from django.http.request import HttpRequest
from django.http.response import JsonResponse


@require_POST
@validate_post_request_body({
    "token": "Authetication token",
    "emailMessage": "Message to be sent ...",
    "recievers": ["List of recievers of this message"]
})
@validateTokenInBody
def test(request: HttpRequest):
    request_dict = json.loads(request.body.decode("utf-8"))

    with EmailClient() as client:
        if "is_html" in request_dict and request_dict["is_html"]:
            client.send_mail(
                request_dict["emailMessage"], *request_dict["recievers"], is_html=True)
        else:
            client.send_mail(
                request_dict["emailMessage"], *request_dict["recievers"], is_html=False)
    return JsonResponse({
        "emailMessage": request_dict["emailMessage"],
    })
