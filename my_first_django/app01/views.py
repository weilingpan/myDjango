from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
import django_rq
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.decorators import action

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from app01.core import JobStatusEnum
from app01.core import get_jobs

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

    # get
    def list(self, request):
        """
        新增API的說明可以放在這裡
        """
        return HttpResponse('get list')
    
    # post
    def create(self, request):
        return HttpResponse('create')
    
    # get
    def retrieve(self, request, pk=None):
        return HttpResponse('retrieve by pk')
    
    # delete
    def destroy(self, request, pk=None):
        return HttpResponse('delete by pk')

class JobViewSet(viewsets.ViewSet):
    iam_organization_field = None
    serializer_class = None

    # [GET] http://127.0.0.1:8000/app01/viewset-job/rq-test/?data=test_data
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'data',
                openapi.IN_QUERY,
                description="Data to be processed",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: openapi.Response('Success')}
    )
    @action(detail=False, methods=['POST'], url_path='rq-test')
    def rq_test(self, request):
        from .tasks import example_task
        data = request.GET.get('data', 'default_data')
        job = example_task.delay(data)
        return JsonResponse({'job_id': job.id, 'status': job.get_status()})

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(
        operation_description="This is the example view",
    )
    def custom_action(self, request):
        # http://127.0.0.1:8000/app01/viewset-job/custom_action/
        return Response({"message": "This is a custom action"})

    @swagger_auto_schema(
        deprecated=True,
    )
    @action(detail=False, methods=['get'])
    def list_finished_jobs(self, request):
        from app01.core import get_finished_jobs
        job_ids, jobs = get_finished_jobs()
        job_data = [{
            'id': job.id,
            'status': job.get_status(),
            'created_at': job.created_at,
            'enqueued_at': job.enqueued_at,
            'started_at': job.started_at,
            'ended_at': job.ended_at,
            'result': job.result,
        } for job in jobs]
        return Response({"jobs": job_ids, "detail": job_data})


    @swagger_auto_schema(
        operation_summary='Push job to queue',
        operation_description="Create a job with the given job_id",
        # 自定義API接口的參數格式
        # 如果使用 request_body, func 裡面要使用 request.data.get("parameter_name") 來取得參數
        # 如果使用 manual_parameters, func 裡面要使用 request.GET.get("parameter_name") 來取得參數
        # in_ 參數
        # openapi.IN_BODY: Request 的 Body 中，例如 POST、PUT 等
        # openapi.IN_QUERY: Request 的 query 中，例如 leezheng/?nice=1。
        # openapi.IN_FORM: Request 的 form 中，例如文檔上傳。
        # openapi.IN_PATH: Request 的 path 中，例如 /leezheng/<pk>/。
        # type 參數
        # openapi.TYPE_STRING: 字串。
        # openapi.TYPE_NUMBER: 數值。
        # openapi.TYPE_INTEGER: 整數。
        # openapi.TYPE_BOOLEAN: 布林。
        # openapi.TYPE_ARRAY: 數組 / 列表。
        # openapi.TYPE_OBJECT: 對象 / 字典。
        # openapi.TYPE_FILE: 檔案。
        manual_parameters=[
           openapi.Parameter(
               name='job_id',
               in_=openapi.IN_QUERY,
               description='job id',
               type=openapi.TYPE_STRING,
               required=True,
               deprecated=False,
           ),],
        # request_body=openapi.Schema(
        #     type=openapi.TYPE_OBJECT,
        #     properties={
        #         'object_A': openapi.Schema(
        #             type=openapi.TYPE_STRING,
        #             description='Description of the object_A.'),
        # }),
        responses={
            200: openapi.Response(description='Job created successfully'),
            400: openapi.Response(description='Invalid input')
        }
    )
    @action(detail=False, methods=['POST'])
    def push_job(self, request):
        job_id = request.GET.get("job_id")
        if not job_id:
            return Response(
                {'error': 'job_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST)
        
        queue = django_rq.get_queue('default')
        job = queue.enqueue_call(
            func='app01.tasks.example_task', 
            args=('test_data',),
            job_id = job_id
        )
        return JsonResponse({'job_id': job.id, 'status': job.get_status()})

    
    status_param = openapi.Parameter(
        'job_status', 
        openapi.IN_QUERY, 
        description="Job status", 
        type=openapi.TYPE_STRING, 
        enum=[status.name for status in JobStatusEnum],
        required=True
    )

    @swagger_auto_schema(
        operation_description="List jobs",
        manual_parameters=[status_param],
    )
    @action(detail=False, methods=['get'])
    def list_jobs(self, request):
        status = request.GET.get("job_status")
        job_ids, jobs = get_jobs(status)
        job_data = [{
            'id': job.id,
            'status': job.get_status(),
            'created_at': job.created_at,
            'enqueued_at': job.enqueued_at,
            'started_at': job.started_at,
            'ended_at': job.ended_at,
            'result': job.result,
        } for job in jobs]
        return Response({"jobs": job_ids, "detail": job_data})
