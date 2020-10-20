"""A class used to store each station as a node and its connections"""
import time, array

class StationHandler:
    
    class Station:
        __slots__ = "_station_name", "_connected_stations", "_prev_node", "_next_node"
        
        def __init__(self, station_name: str):
            self._station_name = station_name
            self._connected_stations = {}
            self._prev_node = None
            self._next_node = None
        
        def add_station_connection(self, station_node: object, time_taken: int, train_line: str):
            """ Connects another station to this station object """
            connected_station_infomation = {
                "TIME_TO": time_taken,
                "TRAINLINE": train_line,
                "Station": station_node
            }
            if station_node._station_name in self._connected_stations.keys():
                raise Exception("The station '" + station_node._station_name + \
                                "' is already connected to the station '" + self._station_name + "'")
            else:
                self._connected_stations[station_node._station_name] = connected_station_infomation
        
        def get_station_connection(self, station_name: str) -> dict:
            """ Returns the data about the station connection to another station"""
            station_info = None
            if station_name in self._connected_stations.keys():
                station_info = self._connected_stations[station_name]
            return station_info
                
        
        @property
        def prev_node(self) -> object:
            return self._prev_node

        @prev_node.setter
        def prev_node(self, station_node: object):
            if isinstance(station_node, self.__class__) or station_node is None:
                self._prev_node = station_node
            else:
                raise Exception("Cannout assign a non 'Station' object to prev_node")
        
        @property
        def next_node(self) -> object:
            return self._next_node
        
        @next_node.setter
        def next_node(self, station_node: object):
            if isinstance(station_node, self.__class__) or station_node is None:
                self._next_node = station_node
            else:
                raise Exception("Cannout assign a non 'Station' object to next_node")
        
        @property
        def connected_stations(self) -> dict:
            return self._connected_stations
        
        @property
        def station_name(self) -> str:
            return self._station_name
            
    
    def __init__(self):
        self._head = None
        self._tail = None
        self._length = 0
        # self._head.next_node = self._tail
        # self._tail.prev_node = self._head
        self.__first_letter_frequency = {}

    def add_station_alphabetically(self, station_name: str) -> None:
        station_node = self.Station(station_name)
        direction = self._get_optimal_direction_of_travel(station_name)
        
        # Set starting point
        current_node = self._head
        if direction == -1: current_node = self._tail
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
                # self._tail = self._head
                # self._head = station_node
                # self._head.next_node = self._tail
                # self._tail.prev_node = self._head
                self._head.next_node = self._tail = self._head
                self._tail.prev_node = self._head = station_node
                self._tail.next_node = None
        else:
            # search list for insertion point
            reached_end_of_list = False
            while (direction == 1 and current_node.station_name <= station_name) or \
                (direction == -1 and current_node.station_name >= station_name):
                if current_node.station_name == station_name:
                    raise Exception("Cannot insert duplicate station name")
                else:
                    if direction == 1:
                        # Going from head -> tail
                        if current_node.next_node is None:
                            reached_end_of_list = True
                            break # Reached end of list and couldn't find place to insert, insert to tail
                        else:
                            current_node = current_node.next_node
                    else:
                        # Going from tail -> head
                        if current_node.prev_node is None:
                            reached_end_of_list = True
                            break # Reached start of list and couldn't find place to insert, insert to head
                        else:
                            current_node = current_node.prev_node
            
            if direction == -1 and current_node != self._tail:
                current_node = current_node.next_node # Done to allow same swapping solution to work regardless of direction
            
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
                    if current_node.prev_node is not None:
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
        if first_letter not in self.__first_letter_frequency.keys():
            self.__first_letter_frequency[first_letter] = 1
        else:
            self.__first_letter_frequency[first_letter] += 1
    
    def print_all_stations(self, current_node=None) -> None:
        """ Displays all the station names in order of the linked list """
        if current_node is None: # If starting point not specified, start from the begining
            current_node = self._head
        while current_node is not None:
            print(current_node.station_name)
            current_node = current_node.next_node
    
    def get_station_node_by_name(self, station_name: str) -> Station:
        """ Returns a station object with the matching station name. 
            Will return None if not found """
        direction = self._get_optimal_direction_of_travel(station_name)
        current_node = None
        if direction == 1:
            current_node = self._head
        else:
            current_node = self._tail
        
        while current_node is not None:
            if current_node.station_name == station_name:
                break
            else:
                if direction == 1:
                    current_node = current_node.next_node
                else:
                    current_node = current_node.prev_node
        return current_node
    
    def _get_optimal_direction_of_travel(self, target_station: str) -> int:
        """ Retruns 1 or -1 depending on if you should start from the head or tail
            to reach the target_station the quickest. 
            Returns 1: head, -1: tail """
        first_letter = target_station[0]
        
        # Get total number of stations before target letter
        left_side_total_stations = 0
        for letter in sorted(self.__first_letter_frequency):
            if first_letter > letter:
                left_side_total_stations += self.__first_letter_frequency[letter]
            else: # The else statement has been added for improved efficiency
                break
        
        # Get total number of stations after target letter
        right_side_total_stations = 0
        if first_letter not in self.__first_letter_frequency.keys():
            right_side_total_stations = self.total_stations - left_side_total_stations
        else:
            right_side_total_stations = self.total_stations - (left_side_total_stations + self.__first_letter_frequency[first_letter])
        
        # Deterimine which direction to travel
        direction = 1
        if right_side_total_stations < left_side_total_stations:
            direction = -1
        return direction

        
    
    @property
    def total_stations(self):
        """ Gets the total number of stations in the double linked list """
        # TODO Maybe a more efficient way to get total size
        total = 0
        for letter in self.__first_letter_frequency:
            total += self.__first_letter_frequency[letter]
        return total
        
        

if __name__ == "__main__":
    S = StationHandler()
    stations = ["Adnan", "Adnan1", "Adnan2", "Adnan3", "Cumin", "Brexith", "Brexit"]
    S.add_station_alphabetically("Adnan")
    # S.add_station_alphabetically("Adnan1")
    
    S.add_station_alphabetically("Daibion")
    S.add_station_alphabetically("Adnan1")
    S.add_station_alphabetically("01") # 3
    S.add_station_alphabetically("Cumin") # 3
    S.add_station_alphabetically("Berlin")
    S.add_station_alphabetically("Adnan2")
    S.add_station_alphabetically("Adnan3")
    S.add_station_alphabetically("Adnan4")
    S.add_station_alphabetically("Breath")
    S.add_station_alphabetically("Brexit")
    S.add_station_alphabetically("Denmark")
    S.print_all_stations()
    # x = S.get_station_node_by_name("Breath")
    # S.print_all_stations()
    # print("###############")
    # S.print_all_stations(x)
    # print(S._get_optimal_direction_of_travel("Cumin"))
    
    
    
    