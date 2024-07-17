import django_rq
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework import status, viewsets

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app01.core import JobStatusEnum
from app01.core import get_jobs, get_finished_jobs
from app01.tasks import example_task


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
        data = request.GET.get('data', 'default_data')
        job = example_task.delay(data)
        return JsonResponse({'job_id': job.id, 'status': job.get_status()})

    @action(detail=False, methods=['get'])
    def custom_action(self, request):
        # http://127.0.0.1:8000/app01/viewset-job/custom_action/
        return Response({"message": "This is a custom action"})
    
    @swagger_auto_schema(
        deprecated=True,
    )
    @action(detail=False, methods=['get'])
    def list_finished_jobs(self, request):
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
            'worker_name': job.worker_name,
            'description': job.description,
            'exc_info': job.exc_info
        } for job in jobs]
        return Response({"jobs": job_ids, "detail": job_data})
        

