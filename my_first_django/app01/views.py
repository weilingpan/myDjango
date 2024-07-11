from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
from django.http import HttpResponse

from rest_framework.decorators import api_view

def route1(request):
    print(request.build_absolute_uri())
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

@api_view(['GET'])
@ensure_csrf_cookie
def route2(request):
    print(request.build_absolute_uri())
    return HttpResponse("route2: ensure_csrf_cookie")

# 這個參數是從 URL 路徑中提取的，而不是從查詢參數中提取的
def route3(request, project_token):
    print(request.build_absolute_uri())
    print(f"Project Token: {project_token}")
    if request.GET.get('is_login') == '0':
        return HttpResponse(
            f"Route3: Project Token: {project_token}, is_login is 0")
        #http://127.0.0.1:8000/app01/route3/123/?is_login=0
        #return: Route3: Project Token: 123, is_login is 0
    else:
        return HttpResponse(
            f"Route3: Project Token: {project_token}, no is_login")
        #http://127.0.0.1:8000/app01/route3/123/
        #return: Route3: Project Token: 123, no is_login
#path('route3/<str:project_token>/', views.route3, name='route3')

def route4(request, is_ok=False):
    #path('route4/<str:is_ok>/', views.route4, name='route4'),
    print(request.build_absolute_uri())

    if is_ok:
        return HttpResponse(f"Route4 - is_ok: {is_ok}")
        # http://127.0.0.1:8000/app01/route4/True/
    else:
        return HttpResponse(f"Route4 - is_ok: {is_ok}")
        # http://127.0.0.1:8000/app01/route4/False/

def route5(request):
    #path('route5/', views.route5, name='route5')
    print(request.GET.get('switch'))
    if request.GET.get('switch') == '0':
        return route4(request, is_ok=True)
        #http://127.0.0.1:8000/app01/route5/?switch=0
    else:
        return route4(request, is_ok=False)
        #http://127.0.0.1:8000/app01/route5/

## add api, it can show on swagger ##
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
class HelloWorld(APIView):
    def get(self, request):
        return Response({"message": "Hello, world!"}, status=status.HTTP_200_OK)


# 1. 定義 viewsets, 需包含（如 list、retrieve、create、update、destroy 等）。
# 2. 使用 routers 在 urls.py 註冊
# 3. 在 viewsets 自定義 CRUD API
from rest_framework import status, viewsets
class FirstViewSet(viewsets.ViewSet):
    iam_organization_field = None
    serializer_class = None

    def list(self, request):
        """
        新增API的說明可以放在這裡
        """
        return HttpResponse('myfirstviewset list')
