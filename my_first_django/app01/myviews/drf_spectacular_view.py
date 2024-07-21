from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

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