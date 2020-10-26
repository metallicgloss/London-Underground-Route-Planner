from station_handler import StationHandler

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

                if (
                    (current_station_shortest_time is None or self._route_calculator[connected_station]["SHORTEST_TIME"] is None)
                    or
                    (current_station_shortest_time + quickest_time <
                     self._route_calculator[connected_station]["SHORTEST_TIME"])
                ):
                    self._route_calculator[connected_station] = {
                        'SHORTEST_TIME': current_station_shortest_time + quickest_time,
                        'FROM_STATION': current_station_name,
                        'FROM_TRAIN_LINE': quickest_train_line,
                        'CURRENT_STATION': connected_station,
                    }

            # Remove current station from remaining stations
            remaining_stations.remove(current_station_name)

        route = []

        next_station = self._route_calculator[destination_station_name]
        while next_station["CURRENT_STATION"] != starting_station_name:
            route.append({
                "FROM": next_station["FROM_STATION"],
                "TO": next_station["CURRENT_STATION"],
                "TRAIN_LINE": next_station["FROM_TRAIN_LINE"]
            })
            next_station = self._route_calculator[next_station["FROM_STATION"]]

        return route[::-1]
