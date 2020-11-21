import re
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
    if any(key not in request.GET for key in ("origin_location", "destination_location", "start_time")):
        # Return invalid message
        return JsonResponse(
            {
                'response': 'Missing Required Parameter.'
            },
            safe=True
        )

    for value in request.GET.items():
        # If time input, check formatting.
        if(value[0] == "start_time"):
            if(not re.search("^([0-1]?[0-9]|2[0-3]):[0-5][0,5]$", value[1])):
                # Return invalid message
                return JsonResponse(
                    {
                        'response': 'Invalid Time Format'
                    },
                    safe=True
                )

        # Simple check to ensure parameter is string and within length limits.
        if((not isinstance(value[1], str)) or (3 >= len(value[1])) or (27 <= len(value[1])) or (value[1] is None) or (value[1] == "")):
            # Return invalid message
            return JsonResponse(
                {
                    'response': 'Invalid or Missing Data'
                },
                safe=True
            )

    # Split time into segments.
    start_time = escape(request.GET['start_time']).split(":", 1)

    # Get route data.
    route_data = planner.calculate_route(
        request.GET['origin_location'],
        request.GET['destination_location'],
        (int(start_time[0]) * 60) + int(start_time[1])
    )

    if('response' not in route_data):
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

    else:
        # Return formatted data to the frontend.
        return JsonResponse(
            route_data,
            safe=True
        )
