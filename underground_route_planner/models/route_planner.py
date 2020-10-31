from .station_handler import StationHandler

# --------------------------------------------------------------------------- #
#                                  CONTENTS                                   #
#                            1. Route Planner Class                           #
#                            1.1 Route Planner Class Methods                  #
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
#                            1. Route Planner Class                           #
# --------------------------------------------------------------------------- #


class RoutePlanner:

    # ----------------------------------------------------------------------- #
    #                    1.1 Route Planner Class Methods                      #
    # ----------------------------------------------------------------------- #

    # Initialise the route planner object.
    def __init__(self, station_handler: StationHandler):
        self._station_handler = station_handler
        self._route_calculator = {}

    # Initiaise the calculator, reset values, add all names to the calculator.
    def _initalise_route_calculator(self) -> None:
        self._route_calculator = {}
        station_names = self._station_handler.get_all_station_names()

        # For each station, initialise data structure.
        for station_name in station_names:
            self._route_calculator[station_name] = {
                "SHORTEST_TIME": None,
                "FROM_STATION": None,
                "FROM_TRAIN_LINE": None,
                "CURRENT_STATION": None
            }

    # Returns the route stored in route_calculator as a list of objects to be used by the front end
    def _get_formatted_route(self, starting_station_name: str, destination_station_name: str) -> list:
        route = []
        next_station = self._route_calculator[destination_station_name]
        prev_train_line = ""
        total_travel_time = 0

        while next_station["CURRENT_STATION"] != starting_station_name:
            from_station_node = self._station_handler.get_station_node_by_name(
                next_station["FROM_STATION"]
            )
            to_station_node = self._station_handler.get_station_node_by_name(
                next_station["CURRENT_STATION"]
            )
            station_change = False

            if next_station["FROM_TRAIN_LINE"] != prev_train_line:
                prev_train_line = next_station["FROM_TRAIN_LINE"]
                station_change = True

            route.append({
                "FROM": {
                    "STATION_NAME": next_station["FROM_STATION"],
                    "STATION_LNG": from_station_node.geolocation_coordinates[0],
                    "STATION_LAT": from_station_node.geolocation_coordinates[1]
                },
                "TO": {
                    "STATION_NAME": next_station["CURRENT_STATION"],
                    "STATION_LNG": to_station_node.geolocation_coordinates[0],
                    "STATION_LAT": to_station_node.geolocation_coordinates[1]
                },
                "TRAIN_LINE": next_station["FROM_TRAIN_LINE"],
                "CHANGE_LINE": station_change,
                "TRAVEL_TIME": next_station["TRAVEL_TIME_BETWEEN_STATIONS"]
            })

            # Update total travel time
            total_travel_time += next_station["TRAVEL_TIME_BETWEEN_STATIONS"]

            # Fix route order and determine if train line changes occurred
            route_in_order = route[::-1]

            # Set inital train line
            prev_train_line = route_in_order[0]["TRAIN_LINE"]
            route_in_order[0]["CHANGE_LINE"] = False

            for route_node in route_in_order[1:]:
                station_change = route_node["TRAIN_LINE"] != prev_train_line
                prev_train_line = route_node["TRAIN_LINE"]
                route_node["CHANGE_LINE"] = station_change

            # Set the next station on the route.
            next_station = self._route_calculator[next_station["FROM_STATION"]]

        return {
            "ROUTE": route_in_order,
            "TOTAL_TRAVEL_TIME": total_travel_time
        }

    # Return the route segment formatted for HTML list.
    def get_formatted_html_route(self, station_name: str, underground_line: str, travel_time: int, total_travel_time: int) -> str:
        return (
            "<tr><td>"
            + station_name
            + "</td><td class = '"
            + underground_line.lower()
            + "'>"
            + underground_line
            + "</td><td>"
            + str(total_travel_time)
            + " mins <small>(+"
            + str(travel_time)
            + " mins)</small></td></tr>"
        )

    # Return the route segment formatted for HTML summary.
    def get_formatted_html_summary(self, origin_station: str, destination_station: str, underground_line: str) -> str:
        return (
            "<li>"
            + origin_station
            + " Station to "
            + destination_station
            + " Station - <span class='"
            + underground_line.lower().split(" ", 1)[0]
            + "'>"
            + underground_line
            + " Line </span> </li>"
        )

    # Return the route segment formatted for HTML summary.

    def get_formatted_html_change_summary(self, station_name: str, from_line: str, to_line: str) -> str:
        return (
            "<li>Change at "
            + station_name
            + " from the <span class='"
            + from_line.lower().split(" ", 1)[0]
            + "'>"
            + from_line
            + " Line </span> to the <span class='"
            + to_line.lower().split(" ", 1)[0]
            + "'>"
            + to_line
            + " Line</span></li>"
        )
    # Calculate the quickest route from the starting station to the next station.

    def get_route(self, starting_station_name: str, destination_station_name: str) -> list:
        # Clear previously calculated route
        self._initalise_route_calculator()

        # Get list of unvisited stations
        remaining_stations = self._station_handler.get_all_station_names()

        # Move the starting station to the front of the list
        remaining_stations.remove(starting_station_name)
        remaining_stations.insert(0, starting_station_name)

        # Set starting point time to 0
        self._route_calculator[starting_station_name]["SHORTEST_TIME"] = 0
        self._route_calculator[starting_station_name]["CURRENT_STATION"] = starting_station_name

        # Calculate Dijkstra table
        while len(remaining_stations) != 0:
            # Order remaining stations by smallest time, Place NoneTypes at the end
            current_station_name = ""

            # The if condition is used to increase execution speed and memory efficiency
            not_none_stations = list(
                filter(
                    lambda x: self._route_calculator[x]["SHORTEST_TIME"] is not None, remaining_stations
                )
            )

            not_none_stations = sorted(
                not_none_stations, key=lambda x: self._route_calculator[x]["SHORTEST_TIME"]
            )

            if not_none_stations == []:
                none_type_stations = list(
                    filter(
                        lambda x: self._route_calculator[x]["SHORTEST_TIME"] is None, remaining_stations
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
            ]["SHORTEST_TIME"]

            for connected_station in current_station.connected_stations:
                # Get quickest connection to specific node
                quickest_time_index = current_station.connected_stations[connected_station]["TIME_TO"].index(
                    min(
                        current_station.connected_stations[connected_station]["TIME_TO"]
                    )
                )

                quickest_time = current_station.connected_stations[
                    connected_station]["TIME_TO"][quickest_time_index]

                quickest_train_line = current_station.connected_stations[
                    connected_station]["TRAIN_LINE"][quickest_time_index]

                # Add extra minute if station is not start or destination station
                train_wait_time = 1
                if current_station.station_name == starting_station_name or current_station.station_name == destination_station_name:
                    train_wait_time = 0

                travel_time_between_stations = quickest_time + train_wait_time

                if (
                    (current_station_shortest_time is None or self._route_calculator[connected_station]["SHORTEST_TIME"] is None)
                    or
                    (current_station_shortest_time + travel_time_between_stations <
                     self._route_calculator[connected_station]["SHORTEST_TIME"])
                ):
                    self._route_calculator[connected_station] = {
                        'SHORTEST_TIME': current_station_shortest_time + travel_time_between_stations,
                        'FROM_STATION': current_station_name,
                        'FROM_TRAIN_LINE': quickest_train_line,
                        'CURRENT_STATION': connected_station,
                        "TRAVEL_TIME_BETWEEN_STATIONS": travel_time_between_stations
                    }

            # Remove current station from remaining stations
            remaining_stations.remove(current_station_name)

        return self._get_formatted_route(starting_station_name, destination_station_name)
