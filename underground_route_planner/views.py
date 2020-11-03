from django.shortcuts import render
from django.http import JsonResponse
from django.apps import apps

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
    # Split time into segments.
    start_time = request.GET['start_time'].split(":", 1)

    # Get route data.
    route_data = planner.get_route(
        request.GET['origin_location'],
        request.GET['destination_location'],
        (int(start_time[0]) * 60) + int(start_time[1])
    )

    # Initialise Variables
    sub_total_time = 0
    time_to_station = 0
    origin_of_line = ""
    underground_line = ""
    formatted_route_data = {
        'raw_data': route_data,
        'route_table': '',
        'route_summary': ''
    }

    # For each route in the data, build HTML table content to display and location list.
    for route_index, route in enumerate(route_data['route']):
        # Get the time taken to get to station from last route.
        if (route_index != 0):
            # If not the first station, set time to station from previous route.
            time_to_station = route_data['route'][
                route_index - 1
            ]['travel_time']

        else:
            # First station, set first origin of the line.
            origin_of_line = route['from']
            underground_line = route['train_line']

        # Create list table entry.
        formatted_route_data['route_table'] += planner.get_formatted_html_route(
            route['from'],
            route['train_line'] + " Line",
            time_to_station,
            sub_total_time
        )

        # If change_line flag set, route has changed to the previous route.
        # Add summary line to the data set, reset origin.
        if(route['change_line']):
            # Create summary list entry.
            formatted_route_data['route_summary'] += planner.get_formatted_html_summary(
                origin_of_line,
                route['from'],
                underground_line
            )

            # Create summary list entry.
            formatted_route_data['route_summary'] += planner.get_formatted_html_change_summary(
                route['from'],
                underground_line,
                route['train_line']
            )

            # Reset origin for new underground line.
            origin_of_line = ""

        # If origin of line blank, this is the first route on the new line.
        if(origin_of_line == ""):
            # Set new origin, set line of the route.
            origin_of_line = route['from']
            underground_line = route['train_line']

        # Add travel time from previous station to running total.
        sub_total_time += route['travel_time']

        # If last route in the list.
        if (len(route_data['route']) == (route_index + 1)):
            # Add destination.
            formatted_route_data['route_table'] += planner.get_formatted_html_route(
                route['to'],
                "-",
                route_data['route'][
                    route_index
                ]['travel_time'],
                sub_total_time
            )

            # Create summary list entry.
            formatted_route_data['route_summary'] += planner.get_formatted_html_summary(
                origin_of_line,
                route['to'],
                underground_line
            )

    return JsonResponse(
        formatted_route_data,
        safe=True
    )
