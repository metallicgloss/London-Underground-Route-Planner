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
    sub_total_time = 0
    time_to_station = 0
    origin_of_line = ""
    underground_line = ""
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
            time_to_station = route_data['ROUTE'][
                route_index - 1
            ]['TRAVEL_TIME']

        else:
            # First station, set first origin of the line.
            origin_of_line = route['FROM']['STATION_NAME']
            underground_line = route['TRAIN_LINE']

        # Create list table entry.
        formatted_route_data['TABLE_OUTPUT'] += planner.get_formatted_html_route(
            route['FROM']['STATION_NAME'],
            route['TRAIN_LINE'] + " Line",
            time_to_station,
            sub_total_time
        )

        # If CHANGE_LINE flag set, route has changed to the previous route.
        # Add summary line to the data set, reset origin.
        if(route['CHANGE_LINE']):
            # Create summary list entry.
            formatted_route_data['SUMMARY_OUTPUT'] += planner.get_formatted_html_summary(
                origin_of_line,
                route['FROM']['STATION_NAME'],
                underground_line
            )

            # Create summary list entry.
            formatted_route_data['SUMMARY_OUTPUT'] += planner.get_formatted_html_change_summary(
                route['FROM']['STATION_NAME'],
                underground_line,
                route['TRAIN_LINE']
            )

            # Reset origin for new underground line.
            origin_of_line = ""

        # If origin of line blank, this is the first route on the new line.
        if(origin_of_line == ""):
            # Set new origin, set line of the route.
            origin_of_line = route['FROM']['STATION_NAME']
            underground_line = route['TRAIN_LINE']

        # Add travel time from previous station to running total.
        sub_total_time += route['TRAVEL_TIME']

        # Add pathway to locations for mapping.
        formatted_route_data['LOCATION_DATA'].append(
            {
                'LONGITUDE': route['FROM']['STATION_LNG'],
                'LATITUDE': route['FROM']['STATION_LAT'],
                'CSS_COLOR_VARIABLE': "--" + route['TRAIN_LINE'].lower().split(" ", 1)[0] + "-line"
            }
        )

        # If last route in the list.
        if (len(route_data['ROUTE']) == (route_index + 1)):
            # Add destination.
            formatted_route_data['TABLE_OUTPUT'] += planner.get_formatted_html_route(
                route['TO']['STATION_NAME'],
                "-",
                time_to_station,
                sub_total_time
            )

            # Create summary list entry.
            formatted_route_data['SUMMARY_OUTPUT'] += planner.get_formatted_html_summary(
                origin_of_line,
                route['TO']['STATION_NAME'],
                underground_line
            )

            # Add pathway to locations for mapping.
            formatted_route_data['LOCATION_DATA'].append(
                {
                    'LONGITUDE': route['TO']['STATION_LNG'],
                    'LATITUDE': route['TO']['STATION_LAT'],
                    'CSS_COLOR_VARIABLE': "--" + route['TRAIN_LINE'].lower().split(" ", 1)[0] + "-line"
                }
            )

    return JsonResponse(
        formatted_route_data,
        safe=True
    )
