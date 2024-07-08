from django.urls import path
from . import views

urlpatterns = [
    path('route1/', views.route1, name='myroute1'),
    path('route2/', views.route2, name='route2'),
    path('route3/<str:project_token>/', views.route3, name='route3')
]
