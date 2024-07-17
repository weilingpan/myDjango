from django.http import HttpResponse, JsonResponse
from rest_framework import status, viewsets

# 1. 定義 viewsets, 需包含（如 list、retrieve、create、update、destroy 等）。
# 2. 使用 routers 在 urls.py 註冊
# 3. 在 viewsets 自定義 CRUD API
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
