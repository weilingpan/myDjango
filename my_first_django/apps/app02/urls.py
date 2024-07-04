from django.urls import path
from . import views

urlpatterns = [
    path('route1/', views.route1, name='myroute1'),
]
