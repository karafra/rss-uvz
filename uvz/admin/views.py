
from django.shortcuts import render
from django.http.request import HttpRequest
from uvz.auth.functions import generate_auth_token
from uvz.models.emailAddresses import EmailAddresses
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login
from django.views.decorators.http import require_GET, require_http_methods


@require_http_methods(["GET", "POST"])
def index(request: HttpRequest):
    next_, username, password = "", "", ""

    if request.GET:
        next_ = request.GET.get('next', "")
    if request.POST:
        username = request.POST.get("username", "")
        password = request.POST.get('password', "")
        user = authenticate(username=username, password=password)
        if user:
            django_login(request, user)
            response = HttpResponseRedirect(
                next_ or "/console/", {"emails": EmailAddresses.objects.all()})
            response.set_cookie("token", generate_auth_token(
                username, password, expiration=2), httponly=True)
            response.set_cookie("refreshToken", generate_auth_token(
                username, password, expiration=3600), httponly=True)
            return response
    return render(
        request,
        "index.html", {
            'username': username,
            'next': next_,
        }
    )


@require_GET
@login_required()
def console(request: HttpRequest):
    return render(request, "console.html", {"emails": EmailAddresses.objects.all()})
