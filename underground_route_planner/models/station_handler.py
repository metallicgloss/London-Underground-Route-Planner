import time
from array import array

# --------------------------------------------------------------------------- #
#                                  CONTENTS                                   #
#                            1. Station Handler Class                         #
#                            1.1 Station Class                                #
#                            1.2 Station Class Methods                        #
#                            1.3 Station Handler Class Methods                #
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
#                            1. Station Handler Class                         #
# --------------------------------------------------------------------------- #

class StationHandler:

    # ----------------------------------------------------------------------- #
    #                          1.1 Station Class                              #
    # ----------------------------------------------------------------------- #

    class Station:
        __slots__ = [
            "_station_name",
            "_geolocation_coordinates",
            "_connected_stations",
            "_prev_node",
            "_next_node"
        ]

        # ------------------------------------------------------------------- #
        #                      1.2 Station Class Methods                      #
        # ------------------------------------------------------------------- #

        # Initialise the station class, accepting input of the station name.
        def __init__(self, station_name: str):
            self._station_name = station_name
            self._geolocation_coordinates = []
            self._connected_stations = {}
            self._prev_node = None
            self._next_node = None

        # Create a connection to a new station object, include the time table and trainline.
        def add_station_connection(self, station_node: object, time_taken: int, train_line: str, bidirectional=True):
            # bidirectional defaulted to true to prevent need for creating a connection in opposite direction.

            station_name = station_node.station_name

            if station_name in self._connected_stations.keys():
                # Check connection does not already exist
                if self._connected_stations[station_name]["TRAIN_LINE"] == train_line and \
                        self._connected_stations[station_name]["STATION_NODE"] == station_node:
                    # Connection already exists.
                    raise Exception(
                        "Attempted to create a duplicate connection.")
                else:
                    # Append new values to connections - append rather than set to enable multiple connections from a single station.
                    self._connected_stations[station_name]["TIME_TO"].append(
                        time_taken
                    )
                    self._connected_stations[station_name]["TRAIN_LINE"].append(
                        train_line
                    )
                    self._connected_stations[station_name]["STATION_NODE"].append(
                        station_node
                    )

            else:
                # Connection already exists, update data.
                connected_station_information = {
                    "TIME_TO": array("i", [time_taken]),
                    "TRAIN_LINE": [train_line],
                    "STATION_NODE": [station_node]
                }
                self._connected_stations[station_name] = connected_station_information

            # Add the station in the opposite direction
            if bidirectional and self._station_name not in station_node.connected_stations:
                station_node.add_station_connection(
                    self, time_taken, train_line
                )

        # Returns the data about the station connection to another station.
        def get_station_connection(self, station_name: str) -> dict:
            station_info = None

            # If station has connections
            if station_name in self._connected_stations.keys():
                station_info = self._connected_stations[station_name]

            return station_info

        # Return previous station object.
        @property
        def prev_node(self) -> object:
            return self._prev_node

        # Set the previous station object.
        @prev_node.setter
        def prev_node(self, station_node: object):
            # If station is an instance of object or none.
            if isinstance(station_node, self.__class__) or station_node is None:
                self._prev_node = station_node

            else:
                raise Exception(
                    "Cannout assign a non 'Station' object to prev_node"
                )

        # Return next station object.
        @property
        def next_node(self) -> object:
            return self._next_node

        # Set the next station object.
        @next_node.setter
        def next_node(self, station_node: object):
            # If station is an instance of object or none.
            if isinstance(station_node, self.__class__) or station_node is None:
                self._next_node = station_node
            else:
                raise Exception(
                    "Cannout assign a non 'Station' object to next_node"
                )

        # Return the dictionary of connected station objects.
        @property
        def connected_stations(self) -> dict:
            return self._connected_stations

        # Return the station name of the object.
        @property
        def station_name(self) -> str:
            return self._station_name

        # Return the geolocation coordinates of the object.
        @property
        def geolocation_coordinates(self) -> list:
            return self._geolocation_coordinates

        # Set the geolocation coordinates of the station object.
        @geolocation_coordinates.setter
        def geolocation_coordinates(self, longitude: float, latitude: float):
            self._geolocation_coordinates = [longitude, latitude]

    # ----------------------------------------------------------------------- #
    #                    1.3 Station Handler Class Methods                    #
    # ----------------------------------------------------------------------- #

    # Initialise the station object.
    def __init__(self):
        self._head = None
        self._tail = None
        self._length = 0
        self.__first_letter_frequency = {}

    # Insert a new station into the double linked list in alphabetical order.
    def add_station_alphabetically(self, station_name: str) -> None:
        station_node = self.Station(station_name)
        direction = self.get_optimal_direction_of_travel(station_name)

        # Set starting point
        current_node = self._head

        # If direction is reversed, set current node to tail.
        if direction == -1:
            current_node = self._tail

        # Find Insertion Point
        if self._head is self._tail is None:
            # Head and Tail not set, set head
            self._head = station_node

        elif self._head is not None and self._tail is None:
            # Head set but not tail. Set tail and re arrange if needed
            if self._head.station_name < station_name:
                # head is before tail, set tail
                station_node.prev_node = self._head
                self._tail = station_node
                self._head.next_node = self._tail

            elif self._head.station_name == station_name:
                # Duplicate station name found
                raise Exception("Cannot insert duplicate station name")

            else:
                # Switch head and tail
                self._head.next_node = self._tail = self._head
                self._tail.prev_node = self._head = station_node
                self._tail.next_node = None

        else:
            # search list for insertion point
            reached_end_of_list = False
            while (direction == 1 and current_node.station_name <= station_name) or \
                    (direction == -1 and current_node.station_name >= station_name):
                # If the current node has the same name as the new station name.
                if current_node.station_name == station_name:
                    raise Exception("Cannot insert duplicate station name")

                else:
                    if direction == 1:
                        # Going from head -> tail
                        if current_node.next_node is None:
                            # Reached end of list and couldn't find place to insert, insert to tail
                            reached_end_of_list = True
                            break
                        else:
                            current_node = current_node.next_node
                    else:
                        # Going from tail -> head
                        if current_node.prev_node is None:
                            # Reached start of list and couldn't find place to insert, insert to head
                            reached_end_of_list = True
                            break

                        else:
                            current_node = current_node.prev_node

            if direction == -1 and current_node != self._tail:
                # Done to allow same swapping solution to work regardless of direction
                current_node = current_node.next_node

            # Insert into double linked list
            if direction == 1:
                if current_node.station_name == self._head.station_name and station_name < self._head.station_name:
                    # insert record before head
                    station_node.next_node = self._head
                    self._head.prev_node = station_node
                    self._head = station_node

                else:
                    # Insert middle
                    station_node.next_node = current_node
                    station_node.prev_node = current_node.prev_node

                    # If the previous node isn't defined.
                    if current_node.prev_node is not None:
                        # Set the next node to be the station.
                        current_node.prev_node.next_node = station_node
                        current_node.prev_node = station_node

            else:
                if current_node.station_name == self._tail.station_name and station_name > self._tail.station_name:
                    # insert record after tail
                    station_node.prev_node = self._tail
                    self._tail.next_node = station_node
                    self._tail = station_node

                else:
                    # Insert middle
                    station_node.next_node = current_node
                    station_node.prev_node = current_node.prev_node
                    current_node.prev_node.next_node = station_node
                    current_node.prev_node = station_node

        # Add first letter to first_letter_frequency
        first_letter = station_name[0]

        # If first letter isn't in the frequency list.
        if first_letter not in self.__first_letter_frequency.keys():
            self.__first_letter_frequency[first_letter] = 1
        else:
            self.__first_letter_frequency[first_letter] += 1

        self._length += 1

    # Print list of all stations in order of linked list. Used primarily in backend testing environment.
    def print_all_stations(self, current_node=None) -> None:
        # If starting point not specified, start from the begining
        if current_node is None:
            current_node = self._head

        while current_node is not None:
            print(current_node.station_name)
            current_node = current_node.next_node

    # Get station object by name, else none if not found.
    def get_station_node_by_name(self, station_name: str):
        # Get the direction of travel that is optimal.
        direction = self.get_optimal_direction_of_travel(station_name)
        current_node = None

        if direction == 1:
            current_node = self._head
        else:
            current_node = self._tail

        while current_node is not None:
            # If the current node is the station, break, else continue in the direction.
            if current_node.station_name == station_name:
                break

            else:
                if direction == 1:
                    current_node = current_node.next_node

                else:
                    current_node = current_node.prev_node

        return current_node

    # Get the optimial direction of travel. Returns 1 or -1 depending on if you should start from the head or tail to reach target.
    def get_optimal_direction_of_travel(self, target_station: str) -> int:
        first_letter = target_station[0]

        # Get total number of stations before target letter
        left_side_total_stations = 0

        for letter in sorted(self.__first_letter_frequency):
            if first_letter > letter:
                left_side_total_stations += self.__first_letter_frequency[letter]
            else:
                # The else statement has been added for improved efficiency
                break

        # Get total number of stations after target letter
        right_side_total_stations = 0

        if first_letter not in self.__first_letter_frequency.keys():
            right_side_total_stations = self.total_stations - left_side_total_stations

        else:
            right_side_total_stations = self.total_stations - \
                (left_side_total_stations +
                 self.__first_letter_frequency[first_letter])

        # Deterimine which direction to travel
        direction = 1
        if right_side_total_stations < left_side_total_stations:
            direction = -1

        return direction

    # Returns the total number of station stored in the list.
    @property
    def total_stations(self):
        return self._length

    # Returns the names of all of the stations stored in the list. Used primarily in backend testing environment.
    def get_all_station_names(self) -> list:
        # Set the start position and get the node.
        self.set_pointer(1)
        station_name = []
        current_station = self.get_current_station()

        # While not at end of list, get the next station.
        while current_station is not None:
            station_name.append(current_station.station_name)
            current_station = self.get_next_station()

        return station_name

    # Return the next station object. Will return none if at the end.
    def get_next_station(self) -> object:
        if self._pointer is not None:
            self._pointer = self._pointer.next_node

        return self._pointer

    # Return the previous station object. Will return none if at the start.
    def get_prev_station(self) -> object:
        if self._pointer is not None:
            self._pointer = self._pointer.prev_node

        return self._pointer

    # Gets the current station at the pointer location.
    def get_current_station(self) -> object:
        return self._pointer

    # Set the pointer at the head (1) or tail (-1)
    def set_pointer(self, direction=-1) -> None:
        if direction == 1:
            self._pointer = self._head

        elif direction == -1:
            self._pointer = self._tail

        else:
            raise Exception("Invalid value for direction parameter")
