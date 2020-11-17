from django.apps import AppConfig
from underground_route_planner.models.route_planner import RoutePlanner
from underground_route_planner.models.data_handler import DataHandler


class UndergroundRoutePlannerConfig(AppConfig):
    name = 'underground_route_planner'

    def __init__(self, app_name, app_module):
        super(
            UndergroundRoutePlannerConfig,
            self
        ).__init__(app_name, app_module)

        self.route_planner = None
        self.data_handler = None

    # Executes only once on program startup after software has been initialised.
    def ready(self):
        # Display startup message.
        print('---------------------------------------\nProgram Initialisation In Progress...\n---------------------------------------')

        # Initialise Data Handler Object and Import Data
        self.data_handler = DataHandler()

        # Execute data import - returns station handler object.
        self.imported_data = self.data_handler.import_station_data()

        # Initialise Route Planner Object
        self.route_planner = RoutePlanner(
            self.imported_data,
            self.data_handler.route_speed_factors,
            self.data_handler.route_geocoding_status,
            self.data_handler.train_run_times
        )