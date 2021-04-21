import json
from uvz.models.emailAddresses import EmailAddresses
from uvz.utilities.decorators import validate_token_in_body
from django.http.request import HttpRequest
from uvz.models.recordModel import RecordRSS
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, JsonResponse
from uvz.utilities.decorators import validate_request_body
from django.views.decorators.http import require_POST, require_http_methods
from django.db.models import Q


@require_POST
@validate_request_body()
@validate_token_in_body
def read_rss_from_database(request: HttpRequest):
    out = []
    if "pageSize" in (json_response := json.loads(request.body.decode("utf-8"))):
        all_records = RecordRSS.objects.all()
        for i in range(min(len(all_records), int(json_response["pageSize"]))):
            out.append(model_to_dict(all_records[i]))

        return JsonResponse(out, safe=False)
    for index, record in enumerate(RecordRSS.objects.all()):
        out.append(model_to_dict(record))
        if index == 10:
            return JsonResponse(out, safe=False)
    return JsonResponse(out, safe=False)


@require_http_methods(["PUT"])
@validate_request_body(sample_body={
    "token": "Authentication token (optional)",
    "record": {
        "published": "Time the record was published",
        "link": "link to full article",
        "description": "Short description of article",
        "title": "Title of article",
    }
})
@validate_token_in_body
def insert_record(request: HttpRequest):
    json_record = json.loads(request.body.decode("utf-8"))["record"]
    if len(list(RecordRSS.objects.all())) > 9:
        (RecordRSS.objects.all()[0]).delete()
        insert_record(request)
    else:
        RecordRSS(
            published=json_record["published"],
            link=json_record["link"],
            description=json_record["description"],
            title=json_record["title"]
        ).save()
    return JsonResponse(json_record)


@require_http_methods(["PUT"])
@validate_request_body(sample_body={
    "token": "Authentication token",
    "email": "Email address to add",
    "nameOfUser": "Name of user to add"
})
@validate_token_in_body
def insert_email(request: HttpRequest):
    body = json.loads(request.body)
    address = EmailAddresses.objects.filter(Q(email=body.get("email")))
    if address:
        return JsonResponse({
            "error": "Email address is already in database"
        })
    EmailAddresses(
        email=body.get("email"),
        name=body.get("nameOfUser")
    ).save()
    return JsonResponse({
        "email": body.get("email")
    })


@require_http_methods(["DELETE"])
@validate_request_body(sample_body={
    "token": "Authentication token (optional)",
    "email": "Email address to delete"
})
@validate_token_in_body
def delete_email(request: HttpRequest):
    body = json.loads(request.body)
    address = EmailAddresses.objects.filter(Q(email=body.get("email")))
    if not address:
        return JsonResponse({
            "error": "Email address is not in database"
        })
    address.delete()
    return JsonResponse({
        "email": body.get("email")
    })



@require_POST
@validate_request_body()
@validate_token_in_body
def read_emails_from_database(request: HttpRequest):
    out = []
    if "pageSize" in (json_response := json.loads(request.body.decode("utf-8"))):
        all_emails = EmailAddresses.objects.all()
        for i in range(min(len(all_emails), int(json_response["pageSize"]))):
            out.append(model_to_dict(all_emails[i]))
        return JsonResponse(out, safe=False)
    for index, record in enumerate(EmailAddresses.objects.all()):
        out.append(model_to_dict(record))
        if index == 10:
            return JsonResponse(out, safe=False)
    return JsonResponse(out, safe=False)
