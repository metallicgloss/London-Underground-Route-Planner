import os
import pandas as pd
from django.apps import AppConfig
from underground_route_planner.models.station_handler import StationHandler


class UndergroundRoutePlannerConfig(AppConfig):
    name = 'underground_route_planner'

    def __init__(self, app_name, app_module):
        super(
            UndergroundRoutePlannerConfig,
            self
        ).__init__(app_name, app_module)
        self.station_handler = None

    # Executes only once on program startup after software has been initialised.
    def ready(self):
        self.station_handler = StationHandler()

        # General data sanitization, returns a pandas dataframe with the sanitized data.
        # Reading the Excel Sheet, and renaming the DataFrame Columns.
        data = pd.read_excel(
            os.path.abspath("London Underground Data.xlsx")
        )
        data.columns = ["Line", "Origin", "Destination", "Time"]

        for i in range(len(data.index)):
            # Sanitizing the missing underground lines, by comparing to the route before and after

            # If "Line" field is null and the underground line for the route above and below route is the same.
            if (pd.isna(data["Line"].iloc[i]) and (data["Line"].iloc[i-1] == data["Line"].iloc[i+1])):
                # Set the underground line of the route to match the same line of the route below.
                data.at[i, "Line"] = data["Line"].iloc[i+1]

            # Attempt strip of spaces from start or end of station name; only attempt if string (not null, not int or any other invalid value)
            if type(data.at[i, "Line"]) is str:
                data.at[i, "Line"] = data["Line"].iloc[i].strip(" ")
            if type(data.at[i, "Origin"]) is str:
                data.at[i, "Origin"] = data["Origin"].iloc[i].strip(" ")
            if type(data.at[i, "Destination"]) is str:
                data.at[i, "Destination"] = data["Destination"].iloc[i].strip(
                    " ")

            # Insert station; if exception raised, station added or problem.
            try:
                self.station_handler.add_station_alphabetically(
                    data["Origin"].iloc[i])
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
                    origin.add_station_connection(destination, int(
                        data["Time"].iloc[i]), data["Line"].iloc[i])
                except Exception:
                    pass
