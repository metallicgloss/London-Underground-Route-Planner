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
    # Get route data.
    route_data = planner.get_route(
        request.GET['origin_location'],
        request.GET['destination_location']
    )

    # Initialise Variables
    subTotalTime = 0
    timeToStaton = 0
    formatted_route_data = {
        'RAW_DATA': route_data,
        'TABLE_OUTPUT': '',
        'SUMMARY_OUTPUT': '',
        'LOCATION_DATA': []
    }

    # For each route in the data, build HTML table content to display and location list.
    for route_index, route in enumerate(route_data['ROUTE']):
        # Get the time taken to get to station from last route.
        if (route_index != 0):
            # If not the first station, set time to station from previous route.
            timeToStaton = route_data['ROUTE'][route_index - 1]['TRAVEL_TIME']

        # Create table entry.
        formatted_route_data['TABLE_OUTPUT'] += (
            "<tr><td>"
            + route['FROM']['STATION_NAME']
            + "</td><td class = "
            + route['TRAIN_LINE'].lower()
            + ">"
            + route['TRAIN_LINE']
            + " Line</td><td>"
            + str(subTotalTime)
            + " mins <small>(+"
            + str(timeToStaton)
            + " mins)</small></td></tr>"
        )

        # Add travel time from previous station to running total.
        subTotalTime += route['TRAVEL_TIME']

        # If last route in the list.
        if (len(route_data['ROUTE']) == (route_index + 1)):
            # Add destination.
            formatted_route_data['TABLE_OUTPUT'] += (
                "<tr><td>"
                + route['TO']['STATION_NAME']
                + "</td><td>-</td><td>"
                + str(subTotalTime)
                + " mins <small>(+"
                + str(timeToStaton)
                + " mins)</small></td></tr>"
            )

        # Add pathway to locations for mapping.
        formatted_route_data['LOCATION_DATA'].append(
            {
                'LONGITUDE': route['FROM']['STATION_LNG'],
                'LATITUDE': route['FROM']['STATION_LAT'],
                'CSS_COLOR_VARIABLE': "--" + route['TRAIN_LINE'].lower().split(" ", 1)[0] + "-line"
            }
        )

    return JsonResponse(
        formatted_route_data,
        safe=True
    )
