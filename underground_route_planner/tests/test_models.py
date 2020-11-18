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
#                            2.1 Initialise Test Data                         #
#                            2.2 Test Single Hop Route                        #
#                            2.3 Test Multi Hop Route                         #
#                            2.4 Test Time Change Difference                  #
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
                "Bank Underground Station",
                "Elephant & Castle Underground Station",
                "South Ealing Underground Station",
                "South Kensington Underground Station"
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
            "Bank Underground Station"
        )
        destination = self.station_handler.get_station_node_by_name(
            "Elephant & Castle Underground Station"
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
                "Bank Underground Station"
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
#                            2. RoutePlanner Tests                            #
# --------------------------------------------------------------------------- #

class RoutePlannerTester(TestCase):

    # ----------------------------------------------------------------------- #
    #                        2.1 Initialise Test Data                         #
    # ----------------------------------------------------------------------- #

    @classmethod
    def setUpTestData(self):
        # Initialise Station Handler Object
        self.station_handler = StationHandler()

        # Manually add stations to handler for testing.
        self.station_handler.add_station_alphabetically(
            "Elephant & Castle Underground Station"
        )
        self.station_handler.add_station_alphabetically(
            "Bank Underground Station"
        )
        self.station_handler.add_station_alphabetically(
            "South Ealing Underground Station"
        )
        self.station_handler.add_station_alphabetically(
            "South Kensington Underground Station"
        )

        # Manually get station objects.
        bank = self.station_handler.get_station_node_by_name(
            "Bank Underground Station"
        )
        elephant = self.station_handler.get_station_node_by_name(
            "Elephant & Castle Underground Station"
        )
        ealing = self.station_handler.get_station_node_by_name(
            "South Ealing Underground Station"
        )
        kensington = self.station_handler.get_station_node_by_name(
            "South Kensington Underground Station"
        )

        # Manually create connections in both directions.
        # Bank - Elphant - Ealing - Kensington (links back to Bank)
        bank.add_station_connection(elephant, 2, "Bakerloo")
        elephant.add_station_connection(bank, 2, "Bakerloo")
        ealing.add_station_connection(elephant, 2, "Bakerloo")
        elephant.add_station_connection(ealing, 2, "Bakerloo")
        ealing.add_station_connection(kensington, 4, "Bakerloo")
        kensington.add_station_connection(ealing, 4, "Bakerloo")
        kensington.add_station_connection(bank, 7, "Circle")
        bank.add_station_connection(kensington, 7, "Circle")

        # Initialise Route Planner object.
        self.route_planner = RoutePlanner(
            self.station_handler,
            {
                "Bakerloo": {
                    "applied_times": [
                        {
                            "end_time": 16,
                            "start_time": 9
                        },
                        {
                            "end_time": 0,
                            "start_time": 19
                        }
                    ],
                    "factor": 0.5
                },
            },
            False,
            {
                "start": 5,
                "end": 24
            }
        )

        pass

    # ----------------------------------------------------------------------- #
    #                        2.2 Test Single Hop Route                        #
    # ----------------------------------------------------------------------- #

    def test_get_short_route(self):
        print("Method: test_get_short_route.")

        # If route length is 2.
        # Detect if it correctly passes the shortest way instead of through bank.
        self.assertEqual(
            2,
            len(
                self.route_planner.calculate_route(
                    "Elephant & Castle Underground Station",
                    "South Kensington Underground Station",
                    54
                )['route']
            )
        )

    # ----------------------------------------------------------------------- #
    #                        2.3 Test Multi Hop Route                         #
    # ----------------------------------------------------------------------- #

    def test_get_long_route(self):
        print("Method: test_get_long_route.")

        # If route length is 1.
        # Detect if it can find the shortest path or if it still goes in order of insertion.
        self.assertEqual(
            1,
            len(
                self.route_planner.calculate_route(
                    "Bank Underground Station",
                    "South Kensington Underground Station",
                    54
                )['route']
            )
        )

    # ----------------------------------------------------------------------- #
    #                        2.4 Test Time Change Difference                  #
    # ----------------------------------------------------------------------- #

    def test_time_differences(self):
        print("Method: test_get_long_route.")

        # Calculate first route at 00:54
        first_route = self.route_planner.calculate_route(
            "Bank Underground Station",
            "Elephant & Castle Underground Station",
            54
        )['route'][0]['travel_time']

        # Calculate first route at 10:00
        second_route = self.route_planner.calculate_route(
            "Bank Underground Station",
            "Elephant & Castle Underground Station",
            600
        )['route'][0]['travel_time']

        # If the first route and the second route aren't the same, pass test.
        self.assertNotEqual(
            first_route,
            second_route
        )

    # ----------------------------------------------------------------------- #
    #                        2.4 Test Time Change Difference                  #
    # ----------------------------------------------------------------------- #

    def test_route_time_selection_difference(self):
        print("Method: test_route_time_selection_difference.")

        # Route selected - outside of speed up it is quickest to go direct.
        # Within speedup, quicker to pass through Elephant & Castle + Ealing

        # Calculate first route across multiple stations outside of speed up.
        first_route = self.route_planner.calculate_route(
            "Bank Underground Station",
            "South Kensington Underground Station",
            1020
        )

        # Calculate second route across multiple stations inside of speed up.
        second_route = self.route_planner.calculate_route(
            "Bank Underground Station",
            "South Kensington Underground Station",
            600
        )

        # If the first route and the second route aren't the same, pass test.
        self.assertNotEqual(
            first_route,
            second_route
        )
