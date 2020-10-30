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
    
    # Returns the route stored in route_calculator as a list of objects to be used by the front end
    def _get_formatted_route(self, starting_station_name: str, destination_station_name: str) -> list:
        route = []
        next_station = self._route_calculator[destination_station_name]
        prev_train_line = ""
        total_travel_time = 0
        
        while next_station["CURRENT_STATION"] != starting_station_name:
            
            from_station_node = self._station_handler.get_station_node_by_name(next_station["FROM_STATION"])
            to_station_node = self._station_handler.get_station_node_by_name(next_station["CURRENT_STATION"])
            station_change = False
            travel_time_between_stations = 0
            
            # Find travel time between stations, check both stations to determine which station the time was recorded
            if next_station["CURRENT_STATION"] in from_station_node.connected_stations.keys():
                travel_time_between_stations = from_station_node.connected_stations[next_station["CURRENT_STATION"]]["TIME_TO"][0]
            elif next_station["FROM_STATION"] in to_station_node.connected_stations.keys():
                travel_time_between_stations = to_station_node.connected_stations[next_station["FROM_STATION"]]["TIME_TO"][0]
            
            if next_station["FROM_TRAIN_LINE"] != prev_train_line:
                prev_train_line = next_station["FROM_TRAIN_LINE"]
                station_change = True
            
            route.append({
                "FROM": {
                    "STATION_NAME": next_station["FROM_STATION"],
                    "STATION_LAT":from_station_node.geolocation_coordinates[0],
                    "STATION_LNG": from_station_node.geolocation_coordinates[1]
                },
                "TO": {
                    "STATION_NAME": next_station["CURRENT_STATION"],
                    "STATION_LAT":to_station_node.geolocation_coordinates[0],
                    "STATION_LNG": to_station_node.geolocation_coordinates[1]
                },
                "TRAIN_LINE": next_station["FROM_TRAIN_LINE"],
                "CHANGE_LINE": station_change,
                "TRAVEL_TIME": travel_time_between_stations
            })
            
            route = route[::-1]
            
            # Update total travel time
            total_travel_time += travel_time_between_stations
            
            next_station = self._route_calculator[next_station["FROM_STATION"]]
        
        return {
            "ROUTE": route,
            "TOTAL_TRAVEL_TIME": total_travel_time
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

        return self._get_formatted_route(starting_station_name, destination_station_name)

if __name__ == "__main__":
    S = StationHandler()

    S.add_station_alphabetically("A")
    S.add_station_alphabetically("B")
    S.add_station_alphabetically("C")
    S.add_station_alphabetically("D")
    S.add_station_alphabetically("E")

    # Add connections from A
    S.get_station_node_by_name("A").add_station_connection(
        S.get_station_node_by_name("C"), 3, "RED")
    S.get_station_node_by_name("A").geolocation_coordinates = [1, 1]

    S.get_station_node_by_name("A").add_station_connection(
        S.get_station_node_by_name("D"), 4, "RED")

    S.get_station_node_by_name("A").add_station_connection(
        S.get_station_node_by_name("D"), 5, "BLUE")

    # Add connections from B
    S.get_station_node_by_name("B").add_station_connection(
        S.get_station_node_by_name("E"), 3, "BLUE")
    S.get_station_node_by_name("B").geolocation_coordinates = [2, 2]

    # Add connections from C
    S.get_station_node_by_name("C").add_station_connection(
        S.get_station_node_by_name("D"), 2, "BLUE")
    S.get_station_node_by_name("C").geolocation_coordinates = [3, 3]

    S.get_station_node_by_name("C").add_station_connection(
        S.get_station_node_by_name("B"), 14, "RED")

    S.get_station_node_by_name("C").add_station_connection(
        S.get_station_node_by_name("B"), 7, "BLUE")

    # Add connections from D
    S.get_station_node_by_name("D").add_station_connection(
        S.get_station_node_by_name("E"), 2, "RED")
    S.get_station_node_by_name("D").geolocation_coordinates = [4, 4]

    # Add connectiond from E
    S.get_station_node_by_name("E").geolocation_coordinates = [5, 5]
    # There is None
    R = RoutePlanner(S)
    a = R.get_route("E", "A")
    for i in a["ROUTE"]:
        print(i)
    print("TOTAL_TRAVEL_TIME" + str(a["TOTAL_TRAVEL_TIME"])) 