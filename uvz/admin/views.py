from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
import requests
from django.shortcuts import redirect, render
from django.http.request import HttpRequest
from django.views.decorators.http import require_GET, require_http_methods
from django.contrib.auth import authenticate, login as django_login, logout
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext


@require_http_methods(["GET", "POST"])
def index(request: HttpRequest):

    next_, username, password = "", "", ""

    if request.GET:
        next_ = request.GET.get('next', "")
    if request.POST:
        username = request.POST.get("username", "")
        password = request.POST.get('password', "")
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            django_login(request, user)
            if next_ == "":
                return HttpResponseRedirect("/")
            return HttpResponseRedirect(next_)
    return render(
        request,
        "index.html", {
            'username': username,
            'next': next_,
        }
    )


@require_GET
@login_required()
def super_secret_site(request: HttpRequest):
    return render(request, "console.html")


@require_GET
def log_out(request: HttpRequest):
    try:
        logout(request)
        return JsonResponse({
            "logedOut": True
        })
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        })
