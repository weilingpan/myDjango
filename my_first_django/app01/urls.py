from django.urls import path
from . import views

# 註冊 viewset #
from rest_framework import routers
from django.urls import path, include
router = routers.DefaultRouter()
router.register(r'-first', views.FirstViewSet, basename='first')
# 註冊 viewset #

urlpatterns = [
    path('route1/', views.route1, name='myroute1'),
    path('route2/', views.route2, name='route2'),
    path('route3/<str:project_token>/', views.route3, name='route3'),
    path('route4/<str:is_ok>/', views.route4, name='route4'),
    path('route5/', views.route5, name='route5'),

    path('hello/', views.HelloWorld.as_view(), name='hello_world'),

    path('viewswt01', include(router.urls)), # 註冊 viewset

    # rq worker
    path('rq-test/', views.rq_test, name='rq_test'),
    # curl http://localhost:8000/app01/rq-test/?data=test_data

    path('push_job/', views.push_job, name='push_job'),
    # curl http://localhost:8000/app01/push_job/?data=test_data
]
