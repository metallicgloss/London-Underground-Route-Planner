from django.test import TestCase
from underground_route_planner.models.station_handler import StationHandler
from underground_route_planner.models.geocoding import GeoCoding


# --------------------------------------------------------------------------- #
#                                  CONTENTS                                   #
#                            1. GeoCoding Tests                               #
#                            2. StationHandler Tests                          #
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
#                            1. GeoCoding Tests                               #
# --------------------------------------------------------------------------- #

class GeoCodingTester(TestCase):
    # Test setup.
    @classmethod
    def setUpTestData(self):
        # Initialise Geocoding object.
        self.geocoding_element = GeoCoding()
        pass

    # Test to ensure that get co-ordinates function is acting as expected.
    def test_get_waterloo_coordinates(self):
        print("Method: test_get_waterloo_coordinates.")
        self.assertEqual(
            [-0.1134282, 51.5024413],
            self.geocoding_element.get_coordinates(
                "Waterloo Underground Station, London"
            )
        )


# --------------------------------------------------------------------------- #
#                            2. StationHandler Tests                          #
# --------------------------------------------------------------------------- #

class StationHanderTester(TestCase):
    # Test setup.
    @classmethod
    def setUpTestData(self):
        # Initialise Geocoding object.
        self.station_handler = StationHandler()
        pass

    def test_adding_stations(self):
        print("Method: test_adding_stations.")

        # Add example stations.
        self.station_handler.add_station_alphabetically(
            "South Ealing Underground Station"
        )
        self.station_handler.add_station_alphabetically(
            "South Kensington Underground Station"
        )
        self.station_handler.add_station_alphabetically(
            "Elephant & Castle Underground Station"
        )
        self.station_handler.add_station_alphabetically(
            "Bank Underground Station"
        )

        # Pass if get station names returns expected order.
        self.assertEqual(
            [
                'Bank Underground Station',
                'Elephant & Castle Underground Station',
                'South Ealing Underground Station',
                'South Kensington Underground Station'
            ],
            self.station_handler.get_all_station_names()
        )

    def test_station_counting(self):
        print("Method: test_station_counting.")

        # Pass if station quantity matches expected amount.
        self.assertEqual(4, self.station_handler.total_stations)

    def test_optimal_direction(self):
        print("Method: test_optimal_direction.")

        # Pass direction matches expected.
        self.assertEqual(
            1,
            self.station_handler.get_optimal_direction_of_travel(
                "Elephant & Castle Underground Station"
            )
        )
