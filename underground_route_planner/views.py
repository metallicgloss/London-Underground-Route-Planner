from django.shortcuts import render
from django.http import JsonResponse
from django.apps import apps
from django.utils.html import escape
from underground_route_planner.models.html_formatter import HTMLFormatter

# Initialise variable to access the configuration file of the project.
underground_route_planner = apps.get_app_config(
    'underground_route_planner'
)

# Use the stored station handler and route planner with data that has been initialised on startup.
handler = underground_route_planner.imported_data
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
    for value in request.GET.items():
        # Simple check to ensure parameter is string and within length limits.
        if((not isinstance(value[0], str)) and (3 < len(value[0]) < 25)):
            # Return invalid message
            return JsonResponse(
                {
                    'response': 'invalid'
                },
                safe=True
            )

    # Split time into segments.
    start_time = escape(request.GET['start_time']).split(":", 1)

    # Get route data.
    route_data = planner.calculate_route(
        escape(request.GET['origin_location']),
        escape(request.GET['destination_location']),
        (int(start_time[0]) * 60) + int(start_time[1])
    )

    # Generate html formatted data.
    html_data = HTMLFormatter(route_data).format_route()

    # Return formatted data to the frontend.
    return JsonResponse(
        {
            'raw_data': route_data,
            'route_table': html_data['route_table'],
            'route_summary': html_data['route_summary'],
            'route_travel_time': html_data['route_travel_time']
        },
        safe=True
    )
