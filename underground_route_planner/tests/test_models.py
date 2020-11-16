from django.test import TestCase
from underground_route_planner.models.station_handler import StationHandler
from underground_route_planner.models.route_planner import RoutePlanner
from underground_route_planner.models.geocode_handler import GeoCoding


# --------------------------------------------------------------------------- #
#                                  CONTENTS                                   #
#                            1. StationHandler Tests                          #
#                            1.1 Initialise Test Data                         #
#                            1.2 Test Creation of Stations                    #
#                            1.3 Test Creation of Duplicate Station           #
#                            1.4 Test Creation of Connection                  #
#                            1.6 Test Retrieval of Invalid Station            #
#                            1.5 Test Retrieval of Station                    #
#                            1.7 Test Station Count                           #
#                            1.8 Test Optimal Direction                       #
#                            2. RoutePlanner Tests                            #
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
#                            1. StationHandler Tests                          #
# --------------------------------------------------------------------------- #

class StationHanderTester(TestCase):

    # ----------------------------------------------------------------------- #
    #                        1.1 Initialise Test Data                         #
    # ----------------------------------------------------------------------- #

    @classmethod
    def setUpTestData(self):
        # Initialise Station Handler object.
        self.station_handler = StationHandler()

        self.station_handler.add_station_alphabetically(
            "Elephant & Castle Underground Station"
        )
        self.station_handler.add_station_alphabetically(
            "Bank Underground Station"
        )

        pass

    # ----------------------------------------------------------------------- #
    #                        1.2 Test Creation of Stations                    #
    # ----------------------------------------------------------------------- #

    def test_adding_stations(self):
        print("Method: test_adding_stations.")

        # Add additional example stations.
        self.station_handler.add_station_alphabetically(
            "South Ealing Underground Station"
        )
        self.station_handler.add_station_alphabetically(
            "South Kensington Underground Station"
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

    # ----------------------------------------------------------------------- #
    #                        1.3 Test Creation of Duplicate Station           #
    # ----------------------------------------------------------------------- #

    def test_adding_duplicate_station(self):
        print("Method: test_adding_duplicate_station.")

        try:
            # Add example stations.
            self.station_handler.add_station_alphabetically(
                "Elephant & Castle Underground Station"
            )
            # If not raised exception, fail test
            passed = False
        except:
            # Exception raised, pass test.
            passed = True

        # Pass if get station names returns expected order.
        self.assertEqual(
            True,
            passed
        )

    # ----------------------------------------------------------------------- #
    #                        1.4 Test Creation of Connection                  #
    # ----------------------------------------------------------------------- #

    def test_adding_station_connection(self):
        print("Method: test_adding_station_connection.")

        # Get station node object, add station connection.
        origin = self.station_handler.get_station_node_by_name(
            'Bank Underground Station'
        )
        destination = self.station_handler.get_station_node_by_name(
            'Elephant & Castle Underground Station'
        )

        try:
            # Create connection
            origin.add_station_connection(
                destination,
                2,
                "Example Underground Line"
            )
            # If not raised exception, pass test
            passed = True
        except:
            # Exception raised, fail test.
            passed = False

        # Pass if get station names returns expected order.
        self.assertEqual(
            True,
            passed
        )

    # ----------------------------------------------------------------------- #
    #                        1.5 Test Retrieval of Station                    #
    # ----------------------------------------------------------------------- #

    def test_get_valid_station(self):
        print("Method: test_get_valid_station.")

        # Pass if station returns as expected model instance
        self.assertIsInstance(
            self.station_handler.get_station_node_by_name(
                'Bank Underground Station'
            ),
            StationHandler.Station
        )

    # ----------------------------------------------------------------------- #
    #                        1.6 Test Retrieval of Invalid Station            #
    # ----------------------------------------------------------------------- #

    def test_get_invalid_station(self):
        print("Method: test_get_valid_station.")

        # Pass if station returns None
        self.assertEqual(
            None,
            self.station_handler.get_station_node_by_name(
                'Example'
            )
        )

    # ----------------------------------------------------------------------- #
    #                        1.7 Test Station Count                           #
    # ----------------------------------------------------------------------- #

    def test_station_counting(self):
        print("Method: test_station_counting.")

        # Pass if station quantity matches expected amount.
        self.assertEqual(4, self.station_handler.total_stations)

    # ----------------------------------------------------------------------- #
    #                        1.8 Test Optimal Direction                       #
    # ----------------------------------------------------------------------- #

    def test_optimal_direction(self):
        print("Method: test_optimal_direction.")

        # Pass direction matches expected.
        self.assertEqual(
            1,
            self.station_handler.get_optimal_direction_of_travel(
                "Elephant & Castle Underground Station"
            )
        )

# --------------------------------------------------------------------------- #
#                            2. StationHandler Tests                          #
# --------------------------------------------------------------------------- #


class ConfigurationTester(TestCase):
    # Test setup.
    @classmethod
    def setUpTestData(self):
        # Initialise Route Planner Object
        self.station_handler = StationHandler()
        self.route_planner = RoutePlanner(self.station_handler)
        pass

# --------------------------------------------------------------------------- #
#                            3. RoutePlanner Tests                            #
# --------------------------------------------------------------------------- #


class RoutePlannerTester(TestCase):
    # Test setup.
    @classmethod
    def setUpTestData(self):
        # Initialise Route Planner Object
        self.station_handler = StationHandler()
        self.route_planner = RoutePlanner(self.station_handler)
        pass
