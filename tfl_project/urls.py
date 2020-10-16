"""
tfl_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/

"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('tfl_route_planner.urls')),
]
