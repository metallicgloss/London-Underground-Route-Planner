from django.urls import path
from underground_route_planner import views

urlpatterns = [
    path('', views.index, name='index'),
    path('licences', views.licences, name='licences'),
    path('userguide', views.userguide, name='userguide'),
    path('search-station', views.station_search, name='search-station'),
    path('search-route', views.route_search, name='search-route'),
]
