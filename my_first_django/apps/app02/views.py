from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def route1(request):
    return HttpResponse("Hello world! app02 route1")
