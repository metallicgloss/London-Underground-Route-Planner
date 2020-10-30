import os
import json
import pandas as pd
import time
from pathlib import Path
from django.apps import AppConfig
from underground_route_planner.models.station_handler import StationHandler
from underground_route_planner.models.route_planner import RoutePlanner
from underground_route_planner.models.geocoding import GeoCoding


class UndergroundRoutePlannerConfig(AppConfig):
    name = 'underground_route_planner'

    def __init__(self, app_name, app_module):
        super(
            UndergroundRoutePlannerConfig,
            self
        ).__init__(app_name, app_module)
        self.station_handler = None
        self.route_planner = None
        self.geocoder = GeoCoding()
        self.gocoded_coordinates_fetched_data = {}

    # Executes only once on program startup after software has been initialised.
    def ready(self):
        # Display startup message.
        print('---------------------------------------\nProgram Initialisation In Progress...\n---------------------------------------')

        # Initialise Station Hander Object
        self.station_handler = StationHandler()

        # General data sanitization, returns a pandas dataframe with the sanitized data.
        # Reading the Excel Sheet, and renaming the DataFrame Columns.
        data = pd.read_excel(
            os.path.abspath("London Underground Data.xlsx")
        )
        data.columns = ["Line", "Origin", "Destination", "Time"]

        # Handle if geocoded data has been generated before.
        geocoded_data_file = Path("geocoded_data.json")
        if geocoded_data_file.is_file():
            # Attempt load of geolocation data.
            with open('geocoded_data.json') as geocoded_data_file:
                self.gocoded_coordinates_fetched_data = json.load(
                    geocoded_data_file
                )
                gocoded_coordinates_found = True

        else:
            # No geocoded data exists. Program first startup.
            print('---------------------------------------\nNo Geocoded Data Found. Executing Initial Startup....\n---------------------------------------')
            gocoded_coordinates_found = False

        for i in range(len(data.index)):
            # Sanitizing the missing underground lines, by comparing to the route before and after

            # If executing geocode lookup, execute 1 second wait per 40 requests to prevent excessive throttling.
            if(not gocoded_coordinates_found):
                if (i % 40 == 0):
                    time.sleep(1)

            # If "Line" field is null and the underground line for the route above and below route is the same.
            if (pd.isna(data["Line"].iloc[i]) and (data["Line"].iloc[i-1] == data["Line"].iloc[i+1])):
                # Set the underground line of the route to match the same line of the route below.
                data.at[i, "Line"] = data["Line"].iloc[i+1]

            # Attempt strip of spaces from start or end of station name; only attempt if string (not null, not int or any other invalid value)
            if type(data.at[i, "Line"]) is str:
                data.at[i, "Line"] = data["Line"].iloc[i].strip(
                    " "
                )
            if type(data.at[i, "Origin"]) is str:
                data.at[i, "Origin"] = data["Origin"].iloc[i].strip(
                    " "
                )

            if type(data.at[i, "Destination"]) is str:
                data.at[i, "Destination"] = data["Destination"].iloc[i].strip(
                    " "
                )

            # Attempt insert of station; if exists, get geo-location coordinates. If already exists, exception will be raised, skip.
            try:
                self.station_handler.add_station_alphabetically(
                    data["Origin"].iloc[i]
                )

                # Get the origin station object by name.
                origin = self.station_handler.get_station_node_by_name(
                    data["Origin"].iloc[i]
                )

                # If program first startup, query data.
                if(not gocoded_coordinates_found):
                    # Inform User
                    print("Executing geocode request on " +
                          data["Origin"].iloc[i] + "... ",
                          end="",
                          flush=True
                          )

                    # Fetch geo-location co-ordinates for station.
                    origin.geolocation_coordinates = self.geocoder.get_coordinates(
                        data["Origin"].iloc[i] +
                        " Underground Station, Central London"
                    )

                    self.gocoded_coordinates_fetched_data[
                        data["Origin"].iloc[i]
                    ] = origin.geolocation_coordinates

                    # Complete
                    print("[DONE]")
                else:
                    # Set geo-location co-ordinates based off of existing data.
                    origin.geolocation_coordinates = self.gocoded_coordinates_fetched_data[
                        data["Origin"].iloc[i]
                    ]
            except Exception:
                pass

            # If destination is not null
            if not (pd.isna(data["Destination"].iloc[i])):
                # Get the origin station object by name.
                origin = self.station_handler.get_station_node_by_name(
                    data["Origin"].iloc[i]
                )

                # Get the destination station by name.
                destination = self.station_handler.get_station_node_by_name(
                    data["Destination"].iloc[i]
                )

                # Attempt add station connection on the origin to the destination. If exception raised, skip.
                try:
                    origin.add_station_connection(
                        destination,
                        int(
                            data["Time"].iloc[i]
                        ),
                        data["Line"].iloc[i]
                    )
                except Exception:
                    pass

        # If geocoding has taken place, save data to file.
        if(not gocoded_coordinates_found):
            with open('geocoded_data.json', 'w') as geocoded_data_file:
                json.dump(
                    self.gocoded_coordinates_fetched_data,
                    geocoded_data_file
                )

        # Initialise Route Planner Object
        self.route_planner = RoutePlanner(self.station_handler)
