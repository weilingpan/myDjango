from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework import serializers, status
from rest_framework.response import Response

from drf_spectacular.utils import OpenApiExample


class ExampleSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=True,
        allow_null=False,
        help_text="help_text",
    )
    age = serializers.CharField(
        required=False,
        allow_null=True,
        help_text="help_text",
    )
    email = serializers.CharField(
        required=True,
        allow_null=False,
        help_text="help_text",
    )

    #Django REST Framework 默认会对设置 required=True 的字段进行验证，因此你可以避免显式地在 validate 方法中重复这些检查。
    def validate(self, data):
        # if 'name' not in data:
        #     raise serializers.ValidationError({"name": "This field is required."})
        # if 'email' not in data:
        #     raise serializers.ValidationError({"email": "This field is required."})
        return data

@extend_schema(tags=['regina-api'])
@extend_schema_view(
    list=extend_schema(
        description="Detailed description of this endpoint.",
        summary='Method returns a list of requests'),
    create=extend_schema(
        summary='Method calls the function'),
)
class ReginaViewSet(viewsets.ViewSet):
    iam_organization_field = None
    serializer_class = None

    authentication_classes = []  # 不允許任何人認證
    permission_classes = [AllowAny]  # 允許任何人訪問

    # authentication_classes = [TokenAuthentication]  # 使用 Token 認證
    # permission_classes = [IsAuthenticated]  # 只有經過認證的用戶可以訪問

    def get_serializer(self, *args, **kwargs):
        pass

    @method_decorator(ensure_csrf_cookie)
    def list(self, request):
        print("abb")
        return JsonResponse({"message": "Hello world!"})

    def create(self, request):
        print("abb")
        return JsonResponse({"message": "Hello world!"})

    @extend_schema(
        summary="Get custom data",
        description="Retrieve custom data",
        responses={200: 'Custom data'},
        parameters=[
            OpenApiParameter(name='param1', 
                             description='A custom query parameter', 
                             required=False, 
                             type=OpenApiTypes.STR),
            OpenApiParameter(name='param2', 
                             description='A custom query parameter', 
                             required=True, 
                             type=OpenApiTypes.STR),
        ],
    )
    @action(detail=False, methods=['get'], url_path='custom-data')
    @method_decorator(ensure_csrf_cookie)
    def custom_route(self, request):
        return JsonResponse({"message": "This is custom data"})
    

    @extend_schema(
        summary="Get custom auth",
        description="Retrieve custom auth",
        responses={200: 'Custom auth'},
        parameters=[
            OpenApiParameter(name='Authorization', 
                             description='Authorization token', 
                             required=False, 
                             type=OpenApiTypes.STR, 
                             location=OpenApiParameter.HEADER),
            OpenApiParameter(name='SessionID', 
                             description='Session ID', 
                             required=True, 
                             type=OpenApiTypes.STR, 
                             location=OpenApiParameter.HEADER),
        ],
    )
    @action(detail=False, methods=['get'], url_path='custom-auth')
    @method_decorator(ensure_csrf_cookie)
    def custom_auth(self, request):
        # curl http://localhost:8000/regina/api/v2/custom-auth -H "cookie: sessionid=xxxxx"
        authorization = request.headers.get('Authorization', None)
        session_id = request.headers.get('SessionID', None)
        return JsonResponse({"message": "This is custom auth"})
    
    @extend_schema(
        summary="Get custom auth",
        description="Retrieve custom auth",
        responses={200: 'Custom auth'},
        request=ExampleSerializer,
        examples=[
            OpenApiExample(
                'Example 1',
                description='An example input.',
                value={
                    'name': 'John Doe',
                    'age': 30,
                    'email': 'john@example.com'
                },
                request_only=True,
            ),
        ]

    )
    @action(detail=False, methods=['post'], url_path='mycreate')
    def mycreate(self, request):
        serializer = ExampleSerializer(data=request.data)
        if serializer.is_valid():
            # return JsonResponse(request.data)
            return Response(request.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    @extend_schema(
        summary="create with parameters",
        description="Retrieve custom data",
        responses={200: 'Custom data'},
        parameters=[
            OpenApiParameter(name='version', 
                             description='version',
                             required=False,
                             type=OpenApiTypes.INT),
        ],
    )
    @action(detail=False, methods=['post'], url_path='mycreate2/(?P<token>[^/.]+)')
    def mycreate2(self, request, token=None):
        version = int(request.query_params.get('version', None))
        return JsonResponse({"message": {
            f"token": token,
            "version": version
            }
        })
