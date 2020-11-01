import os
import json
import pandas as pd
from pathlib import Path
from .station_handler import StationHandler
from .geocode_handler import GeoCoding

# --------------------------------------------------------------------------- #
#                                  CONTENTS                                   #
#                            1. Data Handler Class                            #
#                            1.1 Data Handler Class Methods                   #
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
#                            1. Data Handler Class                            #
# --------------------------------------------------------------------------- #


class DataHandler:

    # ----------------------------------------------------------------------- #
    #                    1.1 Data Handler Class Methods                       #
    # ----------------------------------------------------------------------- #

    # Initialise the data handler object.
    def __init__(self):
        self._station_handler = StationHandler()
        self._geocode_handler = GeoCoding()
        self._new_geocoded_data = False
        self._configuration_file_name = "route_planner_configuration.json"
        self._software_configuration = {}

        self._fetch_configuration_file()

    # Initialise the program configuration file.
    def _initialise_configuration_file(self):
        # Define default configuration.
        base_configuration = {
            "route_data_file": "London Underground Data.xlsx",
            "route_geocoding": False,
            "route_geocoded_data": {},
            "route_speed_multipliers": {
                "Bakerloo": {
                    "multiplier": 0.5,
                    "applied_times": [
                        {
                            "start_time": 9,
                            "end_time": 16
                        },
                        {
                            "start_time": 19,
                            "end_time": 0
                        }
                    ]
                }
            },
        }

        with open(self._configuration_file_name, 'w') as configuration_data:
            # Write JSON content into the configuration file.
            json.dump(
                base_configuration,
                configuration_data,
                indent=4,
                sort_keys=True
            )

        # Return default configuration.
        return base_configuration

    # Fetch the program configuration file.
    def _fetch_configuration_file(self):
        # Verify configuration file exists.
        configuration_file = Path(self._configuration_file_name)

        if configuration_file.is_file():
            # Configuration file exists, import into the program.
            with open(self._configuration_file_name) as configuration_data:
                # Parse configuration file as json.
                self._software_configuration = json.load(
                    configuration_data
                )
        else:
            # Configuration file does not exist, initialise with basic data structure.
            self._software_configuration = self._initialise_configuration_file()

    # Fetch the speed factors from the configuration file.
    def fetch_route_speed_factors(self):
        return self._software_configuration['route_speed_multipliers']

    # Import provided station data.
    def import_station_data(self):
        # General data sanitization, returns a pandas dataframe with the sanitized data.
        # Reading the Excel Sheet, and renaming the DataFrame Columns.
        data = pd.read_excel(
            os.path.abspath(self._software_configuration['route_data_file'])
        )
        data.columns = ["Line", "Origin", "Destination", "Time"]

        for i in range(len(data.index)):
            try:
                route_data = self._sanitise_route(
                    data["Origin"].iloc[i],
                    data["Destination"].iloc[i],
                    data["Time"].iloc[i],
                    data["Line"].iloc[i-1],
                    data["Line"].iloc[i],
                    data["Line"].iloc[i+1]
                )
            except IndexError:
                route_data = self._sanitise_route(
                    data["Origin"].iloc[i],
                    data["Destination"].iloc[i],
                    data["Time"].iloc[i],
                    "",
                    data["Line"].iloc[i],
                    ""
                )

            # Attempt insert of station; if exists. If already exists, exception will be raised, skip.
            try:
                # Add station to double linked list.
                self._station_handler.add_station_alphabetically(
                    route_data['origin_station']
                )

                # Get the origin station object by name.
                origin = self._station_handler.get_station_node_by_name(
                    route_data['origin_station']
                )

                if(self._software_configuration['route_geocoding']):
                    origin.geolocation_coordinates = self._fetch_geocoded_data(
                        route_data['origin_station']
                    )
                else:
                    # Geocoding disabled, set coordinates to 0.
                    origin.geolocation_coordinates = [0, 0]

            except Exception:
                pass

            # If destination is not null (contains data - a route rather than in the list of stations)
            if not (pd.isna(route_data['destination_station'])):
                # Get the origin station object by name.
                origin = self._station_handler.get_station_node_by_name(
                    route_data['origin_station']
                )

                # Get the destination station by name.
                destination = self._station_handler.get_station_node_by_name(
                    route_data['destination_station']
                )

                # Attempt add station connection on the origin to the destination. If exception raised, skip.
                try:
                    origin.add_station_connection(
                        destination,
                        int(
                            route_data['route_time']
                        ),
                        route_data['route_line']
                    )
                except Exception:
                    pass

        # If new geocoded data has been generated, update configuration file.
        if(self._new_geocoded_data):
            # Write json configuration to file.
            with open(self._configuration_file_name, 'w') as configuration_data:
                json.dump(
                    self._software_configuration,
                    configuration_data,
                    indent=4,
                    sort_keys=True
                )

        return self._station_handler

    # Sanitise a specific route within the imported data.

    def _sanitise_route(self, origin_station: str, destination_station: str, route_time: float, previous_route_line: str, route_line: str, next_route_line: str):
        # If "Line" field is null and the underground line for the route above and below route is the same.
        if (pd.isna(origin_station) and (previous_route_line == next_route_line)):
            # Set the underground line of the route to match the same line of the route below.
            route_line = next_route_line

        # Attempt strip of spaces from start or end of station name; only attempt if string (not null, not int or any other invalid value)
        if type(route_line) is str:
            route_line = route_line.strip(
                ""
            )

        if type(origin_station) is str:
            origin_station = origin_station.strip(
                " "
            )

        if type(destination_station) is str:
            destination_station = destination_station.strip(
                " "
            )

        return {
            'origin_station': origin_station,
            'destination_station': destination_station,
            'route_time': route_time,
            'route_line': route_line,
        }

    # Generate geocoding data for station.
    def _fetch_geocoded_data(self, station_name: str):
        # If station does not have matching geocoded data, generate new.
        if(station_name not in self._software_configuration['route_geocoded_data']):
            self._generate_route_geocoding(station_name)

        return self._software_configuration['route_geocoded_data'][station_name]

    # Generate geocoding data for station.
    def _generate_route_geocoding(self, station_name: str):
        # Set flag that new geocoded data has been generated - requires configuration update.
        self._new_geocoded_data = True

        # Inform User
        print("Executing geocode request on " +
              station_name + "... ",
              end="",
              flush=True
              )

        # Update software configuration data to include new geocoded data.
        self._software_configuration['route_geocoded_data'][station_name] = self._geocode_handler.get_coordinates(
            station_name +
            " Underground Station, Central London"
        )

        # Complete
        print("[DONE]")

    @property
    def route_speed_multipliers(self) -> dict:
        return self._software_configuration["route_speed_multipliers"]
