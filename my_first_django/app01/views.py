from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
from django.http import HttpResponse

def route1(request):
    return HttpResponse("Hello world! app01")

# def route1(request):
#     print(request.GET.keys)
#     project_token = request.GET.get('project_token', None)
#     if project_token:
#         print(f"Project Token: {project_token}")
#         return HttpResponse(f"Hello world! app01, Project Token: {project_token}")
#     else:
#         print("No project token provided")
#         return HttpResponse("Hello world! app01, No project token")
# path('route1/', views.route1, name='myroute1')
# http://127.0.0.1:8000/app01/route1/?project_token=123
# http://127.0.0.1:8000/app01/route1/

@ensure_csrf_cookie
def route2(request):
    return HttpResponse("route2: ensure_csrf_cookie")

# 這個參數是從 URL 路徑中提取的，而不是從查詢參數中提取的
def route3(request, project_token):
    print(f"Project Token: {project_token}")
    return HttpResponse(f"Route3: Project Token: {project_token}")
#http://127.0.0.1:8000/app01/route3/123/
#path('route3/<str:project_token>/', views.route3, name='route3')
