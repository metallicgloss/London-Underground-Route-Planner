from django.urls import path
from tfl_route_planner import views

urlpatterns = [
    path('', views.index, name='index'),
    path('licences', views.licences, name='licences'),
    path('userguide', views.userguide, name='userguide'),
]
