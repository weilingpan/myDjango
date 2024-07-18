"""my_first_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls)
# ]

from django.contrib import admin
from django.urls import include, path

## for swagger ##
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

###### 使用 drf_yasg ######
# 建立 Swagger-OpenAPI 頁面上的基礎信息。
# schema_view = get_schema_view(
#     openapi.Info(
#         title="Your Project API", # [必要] 設置 Swagger-OpenAPI 頁面上的標題。
#         default_version='v1', # [必要] 設置 Swagger-OpenAPI 的默認版本。
#         description="API documentation for your project", # [可選] 設置 Swagger-OpenAPI 頁面上的描述信息。
#         terms_of_service="https://www.google.com/policies/terms/",  # [可選] 設置 Swagger-OpenAPI 文檔服務條款。
#         contact=openapi.Contact(email="regina@example.com"), # [可選] 設置 Swagger-OpenAPI 頁面上的聯絡人信息
#         license=openapi.License(name="BSD License"), # [可選] 設置 Swagger-OpenAPI 文檔許可證信息。
#     ),
#     public=True, # 設置 Swagger-OpenAPI 文檔頁面為任何人都可訪問（不建議在正式環境下啟用）
#     permission_classes=(permissions.AllowAny,), #　內置權限類 permissions.AllowAny，表示任何人都有權限訪問視圖。
# )
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path("app01/", include("app01.urls")),
#     path('django-rq/', include('django_rq.urls')), # for rq-worker

#     ## for swagger ##
#     # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# ]


###### 使用 drf_spectacular ######
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')), # for rq-worker


    path( 'api/schema/' , SpectacularAPIView.as_view(), name= 'schema' ),
    path( 'swagger/' , SpectacularSwaggerView.as_view(url_name= 'schema' ), name= 'swagger-ui' ),
    path( 'redoc/' , SpectacularRedocView.as_view(url_name= 'schema' ), name= 'redoc' ), 

    path("app01/", include("app01.urls")),
]

