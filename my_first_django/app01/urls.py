from django.urls import path
from . import views

urlpatterns = [
    path('route1/', views.route1, name='myroute1'),
    path('route2/', views.route2, name='route2'),
    path('route3/<str:project_token>/', views.route3, name='route3'),
    path('route4/<str:is_ok>/', views.route4, name='route4'),
    path('route5/', views.route5, name='route5'),

    path('hello/', views.HelloWorld.as_view(), name='hello_world'),
]
