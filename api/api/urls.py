from django.http.response import HttpResponse
from django.urls import path

urlpatterns = [
    path("health", lambda r: HttpResponse(b"ok")),
]
