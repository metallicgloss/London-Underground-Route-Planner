from django.urls import path
from tfl_route_planner import views

urlpatterns = [
    path('', views.index, name='index'),
]