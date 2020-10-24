"""A class used to store each station as a node and its connections"""

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
        self._head = self.Station("")
        self._tail = self.Station("")
        self._head.next_node = self._tail
        self._tail.prev_node = self._head
        self._size = 2
    
    def add_station_alphabetically(self, station_name: str) -> None:
        """ Adds a station alphabetically to the double linked list"""
        # Creates a station node using the station name
        station_node = self.Station(station_name)
        current_node = self._head
        
        # Searchs where to add the station node
        while current_node.station_name != "" and current_node.station_name <= station_name:
            if current_node.station_name == station_name:
                raise Exception("Attempted Insert of duplicate station name '" + station_name + "'")
            if current_node.next_node is not None:
                current_node = current_node.next_node
            else:
                break
        
        if current_node.station_name == "": 
            # If station node name not specified, replace the node
            station_node.next_node = current_node.next_node
            station_node.prev_node = current_node.prev_node
            if current_node.prev_node is not None:
                current_node.prev_node.next_node = station_node
            else:
                self._head = station_node
            if current_node.next_node is not None:
                current_node.next_node.prev_node = station_node
            else:
                self._tail = station_node
        elif current_node.station_name <= station_node.station_name:
            # Reached the end of the list
            current_node.next_node = station_node
            self._tail = station_node
        else:
            # Add station node in between two other nodes
            station_node.next_node = current_node
            station_node.prev_node = current_node.prev_node
            
            if current_node.prev_node is not None:
                current_node.prev_node.next_node = station_node
            else:
                self._head = station_node
            
            current_node.prev_node = station_node
            
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
        current_node = self._head
        while current_node is not None:
            if current_node.station_name == station_name:
                break
            else:
                current_node = current_node.next_node
        return current_node

if __name__ == "__main__":
    S = StationHandler()
    S.add_station_alphabetically("Adnan")
    S.add_station_alphabetically("Cumin")
    S.add_station_alphabetically("Breath")
    x = S.get_station_node_by_name("Breath")
    S.print_all_stations()
    print("###############")
    S.print_all_stations(x)
    
    
    