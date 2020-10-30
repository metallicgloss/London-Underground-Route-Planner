from django.shortcuts import render
from django.http import JsonResponse
from django.apps import apps

# Initialise variable to access the configuration file of the project.
underground_route_planner = apps.get_app_config(
    'underground_route_planner'
)

# Use the stored station handler and route planner with data that has been initialised on startup.
handler = underground_route_planner.station_handler
planner = underground_route_planner.route_planner


def index(request):
    return render(request, 'index.html', {})


def licences(request):
    return render(request, 'licences.html')


def userguide(request):
    return render(request, 'userguide.html')


def station_search(request):
    return JsonResponse(
        handler.query_station_names(
            request.GET['station']
        ),
        safe=False
    )


def route_search(request):
    return JsonResponse(
        planner.get_route(
            request.GET['origin_location'],
            request.GET['destination_location']
        ),
        safe=False
    )
