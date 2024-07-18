from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse


@extend_schema(tags=['regina-api'])
@extend_schema_view(
    list=extend_schema(
        summary='Method returns a list of requests'),
    create=extend_schema(
        summary='Method calls the function'),
)
class ReginaViewSet(viewsets.ViewSet):
    iam_organization_field = None
    serializer_class = None

    def get_serializer(self, *args, **kwargs):
        pass

    def list(self, request):
        print("abb")
        return JsonResponse({"message": "Hello world!"})

    def create(self, request):
        print("abb")
        return JsonResponse({"message": "Hello world!"})
