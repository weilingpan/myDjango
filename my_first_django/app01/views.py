from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
from django.http import HttpResponse

def route1(request):
    return HttpResponse("Hello world! app01")

@ensure_csrf_cookie
def route2(request):
    return HttpResponse("route2: ensure_csrf_cookie")
