from django.urls import path
from . import views

from rest_framework import routers
from django.urls import path, include

from .myviews.job_view import JobViewSet
from .myviews.example_view import FirstViewSet


###### 使用 drf_yasg ######
# router = routers.DefaultRouter()
# # router.register(r'-first', views.FirstViewSet, basename='first')
# # router.register(r'-oldjob', views.JobViewSet, basename='oldjob')
# router.register(r'-first', FirstViewSet, basename='first')
# router.register(r'-job', JobViewSet, basename='job')


# urlpatterns = [
#     path('route1/', views.route1, name='myroute1'),
#     path('route2/', views.route2, name='route2'),
#     path('route3/<str:project_token>/', views.route3, name='route3'),
#     path('route4/<str:is_ok>/', views.route4, name='route4'),
#     path('route5/', views.route5, name='route5'),

#     path('hello/', views.HelloWorld.as_view(), name='hello_world'),

#     # app01/myviews/
#     path('viewset', include(router.urls)),
# ]


###### 使用 drf_spectacular ######

urlpatterns = [
    path('route1/', views.route1, name='myroute1'),
    path('route2/', views.route2, name='route2'),
]
