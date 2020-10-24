from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('underground_route_planner.urls')),
]
