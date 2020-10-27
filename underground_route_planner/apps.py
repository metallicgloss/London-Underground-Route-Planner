from django.apps import AppConfig
from underground_route_planner.models.station_handler import StationHandler


class UndergroundRoutePlannerConfig(AppConfig):
    name = 'underground_route_planner'

    def __init__(self, app_name, app_module):
        super(UndergroundRoutePlannerConfig,
              self).__init__(app_name, app_module)
        self.station_handler = None

    # Executes only once on program startup after software has been initialised.
    def ready(self):
        # TODO: Integrate XLSX load.
        self.station_handler = StationHandler()
        self.station_handler.add_station_alphabetically("Berlin")
        self.station_handler.add_station_alphabetically("Adnan2")
        self.station_handler.add_station_alphabetically("Adnan3")
        self.station_handler.add_station_alphabetically("Adnan4")
        self.station_handler.add_station_alphabetically("Breath")
        self.station_handler.add_station_alphabetically("Brexit")
        self.station_handler.add_station_alphabetically("Denmark")
