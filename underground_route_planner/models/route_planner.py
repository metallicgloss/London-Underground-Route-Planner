from math import ceil
from .station_handler import StationHandler

# --------------------------------------------------------------------------- #
#                                  CONTENTS                                   #
#                            1. Route Planner Class                           #
#                            1.1 Initialise Object                            #
#                            1.2 Initialise Calculator                        #
#                            1.3 Calcualte Route                              #
#                            1.4 Generate Route Structure                     #
#                            1.5 Generate Location Structure                  #
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
#                            1. Route Planner Class                           #
# --------------------------------------------------------------------------- #


class RoutePlanner:

    # ----------------------------------------------------------------------- #
    #                        1.1 Initialise Object                            #
    # ----------------------------------------------------------------------- #

    # Initialise the route planner object.
    def __init__(self, station_handler: StationHandler, route_speed_factors: {}, route_geocoding: bool):
        self._station_handler = station_handler
        self._route_speed_factors = route_speed_factors
        self._route_geocoding = route_geocoding
        self._route_calculator = {}

    # ----------------------------------------------------------------------- #
    #                        1.2 Initialise Calculator                        #
    # ----------------------------------------------------------------------- #

    # Initiaise the calculator, reset values, add all names to the calculator.
    def _initalise_route_calculator(self) -> None:
        self._route_calculator = {}
        station_names = self._station_handler.get_all_station_names()

        # For each station, initialise data structure.
        for station_name in station_names:
            self._route_calculator[station_name] = {
                "shortest_time": None,
                "from_station": None,
                "from_train_line": None,
                "current_station": None,
                "travel_time_between_stations": None,
                "time_reached_station": None
            }

    # ----------------------------------------------------------------------- #
    #                        1.3 Calcualte Route                              #
    # ----------------------------------------------------------------------- #

    # Calculate the quickest route from the starting station to the next station.
    def calculate_route(self, starting_station_name: str, destination_station_name: str, journey_start_time_24h_minutes: int) -> list:
        # Checks if the journey time should be altered to due changes made in the configuration
        def check_route_speed_factor_should_apply(current_time_in_minutes: int, train_line: str) -> bool:
            conditon_met = False
            if train_line in self._route_speed_factors:
                for time_intervals in self._route_speed_factors[train_line]["applied_times"]:
                    start_time_in_minutes = time_intervals["start_time"] * 60
                    end_time_in_minutes = time_intervals["end_time"] * 60
                    if current_time_in_minutes >= start_time_in_minutes and current_time_in_minutes <= end_time_in_minutes:
                        conditon_met = True
            return conditon_met

        # Clear previously calculated route
        self._initalise_route_calculator()
        # Get list of unvisited stations
        remaining_stations = self._station_handler.get_all_station_names()

        # Move the starting station to the front of the list
        remaining_stations.remove(starting_station_name)
        remaining_stations.insert(0, starting_station_name)

        # Set starting point time to 0
        self._route_calculator[starting_station_name]["shortest_time"] = 0
        self._route_calculator[starting_station_name]["current_station"] = starting_station_name

        current_time_in_minutes = journey_start_time_24h_minutes
        self._route_calculator[starting_station_name]["time_reached_station"] = current_time_in_minutes

        # Calculate Dijkstra table
        while len(remaining_stations) != 0:
            # Order remaining stations by smallest time, Place NoneTypes at the end
            current_station_name = ""

            # The if condition is used to increase execution speed and memory efficiency
            not_none_stations = list(
                filter(
                    lambda x: self._route_calculator[x]["shortest_time"] is not None, remaining_stations
                )
            )

            not_none_stations = sorted(
                not_none_stations, key=lambda x: self._route_calculator[x]["shortest_time"]
            )

            if not_none_stations == []:
                none_type_stations = list(
                    filter(
                        lambda x: self._route_calculator[x]["shortest_time"] is None, remaining_stations
                    )
                )

                current_station_name = (
                    not_none_stations + none_type_stations
                )[0]

            else:
                current_station_name = not_none_stations[0]

            # Freeing no longer needed memory
            del not_none_stations

            # Cycle Dijkstra Algorithm
            current_station = self._station_handler.get_station_node_by_name(
                current_station_name
            )
            current_station_shortest_time = self._route_calculator[
                current_station_name
            ]["shortest_time"]

            current_time_in_minutes = self._route_calculator[
                current_station_name]["time_reached_station"]

            # Cycle through all stations connected to current station
            for connected_station in current_station.connected_stations:
                # Get quickest connection to specific node
                quickest_time_index = current_station.connected_stations[connected_station]["time_to"].index(
                    min(
                        current_station.connected_stations[connected_station]["time_to"]
                    )
                )

                quickest_time = current_station.connected_stations[
                    connected_station]["time_to"][quickest_time_index]

                quickest_train_line = current_station.connected_stations[
                    connected_station]["train_line"][quickest_time_index]

                # Add extra minute if station is not start or destination station
                train_wait_time = 1
                if current_station.station_name == starting_station_name or current_station.station_name == destination_station_name:
                    train_wait_time = 0

                travel_time_between_stations = 0  # Created just for initalisation purposes

                # Determine if route_speed factor should apply
                if check_route_speed_factor_should_apply(current_time_in_minutes, quickest_train_line):
                    speed_factor = self._route_speed_factors[quickest_train_line]["factor"]
                    travel_time_between_stations = ceil(
                        quickest_time * speed_factor
                    ) + train_wait_time
                else:
                    travel_time_between_stations = quickest_time + train_wait_time

                if (
                    (current_station_shortest_time is None or self._route_calculator[connected_station]["shortest_time"] is None)
                    or
                    (current_station_shortest_time + travel_time_between_stations <
                     self._route_calculator[connected_station]["shortest_time"])
                ):
                    self._route_calculator[connected_station] = {
                        'shortest_time': current_station_shortest_time + travel_time_between_stations,
                        'from_station': current_station_name,
                        'from_train_line': quickest_train_line,
                        'current_station': connected_station,
                        "travel_time_between_stations": travel_time_between_stations,
                        "time_reached_station": current_time_in_minutes + travel_time_between_stations
                    }

            # Remove current station from remaining stations
            remaining_stations.remove(current_station_name)

        return self._generate_route_structure(starting_station_name, destination_station_name)

    # ----------------------------------------------------------------------- #
    #                        1.4 Generate Route Structure                     #
    # ----------------------------------------------------------------------- #

    # Returns the route stored in route_calculator as a list of objects to be used by the front end
    def _generate_route_structure(self, starting_station_name: str, destination_station_name: str) -> list:
        route = []
        route_locations = []
        next_station = self._route_calculator[destination_station_name]
        prev_train_line = ""

        while next_station["current_station"] != starting_station_name:
            station_change = False

            # If geocoding is enabled, handle location formatting.
            if(self._route_geocoding):
                # If route locations empty, currently at destination station (loop works backwards)
                if(route_locations == []):
                    # Fetch destination station node details.
                    to_station_node = self._station_handler.get_station_node_by_name(
                        next_station["current_station"]
                    )

                    # Add pathway to destination location for mapping.
                    route_locations.append(
                        self._generate_location_structure(
                            to_station_node.geolocation_coordinates,
                            next_station["from_train_line"]
                        )
                    )

                # Get the origin station for each route segment.
                from_station_node = self._station_handler.get_station_node_by_name(
                    next_station["from_station"]
                )

                # Add pathway of origin location for mapping.
                route_locations.append(
                    self._generate_location_structure(
                        from_station_node.geolocation_coordinates,
                        next_station["from_train_line"]
                    )
                )

            if next_station["from_train_line"] != prev_train_line:
                prev_train_line = next_station["from_train_line"]
                station_change = True

            route.append({
                "from": next_station["from_station"],
                "to": next_station["current_station"],
                "train_line": next_station["from_train_line"],
                "change_line": station_change,
                "travel_time": next_station["travel_time_between_stations"]
            })

            # Fix route order and determine if train line changes occurred
            route_in_order = route[::-1]

            # Set inital train line
            prev_train_line = route_in_order[0]["train_line"]
            route_in_order[0]["change_line"] = False

            for route_node in route_in_order[1:]:
                station_change = route_node["train_line"] != prev_train_line
                prev_train_line = route_node["train_line"]
                route_node["change_line"] = station_change

            # Set the next station on the route.
            next_station = self._route_calculator[next_station["from_station"]]

        return {
            "route": route_in_order,
            "route_locations": route_locations[::-1]
        }

    # ----------------------------------------------------------------------- #
    #                        1.5 Generate Location Structure                  #
    # ----------------------------------------------------------------------- #

    # Returns the location for processing on frontend Google Maps JS API.
    def _generate_location_structure(self, geolocation_coordinates: list, underground_line: str) -> dict:
        return {
            'longitude': geolocation_coordinates[0],
            'latitude': geolocation_coordinates[1],
            'css_color_variable': "--" + underground_line.lower().split(" ", 1)[0] + "-line"
        }
