import json
from uvz.utilities.decorators import validateTokenInBody
import feedparser
from django.http.request import HttpRequest
from uvz.models.recordModel import RecordRSS
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, JsonResponse
from uvz.utilities.decorators import validate_post_request_body
from django.views.decorators.http import require_POST, require_http_methods


@require_POST
@validate_post_request_body()
@validateTokenInBody
def read_records_from_database(request: HttpRequest):
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
@validate_post_request_body(sample_body={
    "token": "Authentication token",
    "record": {
        "published": "Time the record was published",
        "link": "link to full article",
        "description": "Short description of article",
        "title": "Title of article",
    }
})
@validateTokenInBody
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
