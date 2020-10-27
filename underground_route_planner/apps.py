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
        self.station_handler = StationHandler()
        # TODO: Integrate XLSX load into handler
