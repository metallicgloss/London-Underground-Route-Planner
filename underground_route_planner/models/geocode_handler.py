import googlemaps
from django.db import models

# --------------------------------------------------------------------------- #
#                                  CONTENTS                                   #
#                            1. Geocode Hander Class                          #
#                            1.1 Initialise Object                            #
#                            1.2 Get Coordinates                              #
# --------------------------------------------------------------------------- #


class GeoCoding:

    # ----------------------------------------------------------------------- #
    #                        1.1 Initialise Object                            #
    # ----------------------------------------------------------------------- #

    def __init__(self, route_geocoding_api_key):
        # Define internal variable for google map connection.
        self._google_map_connection = googlemaps.Client(
            key=route_geocoding_api_key
        )

    # ----------------------------------------------------------------------- #
    #                        1.2 Get Coordinates                              #
    # ----------------------------------------------------------------------- #

    # Return coordinates for address query.
    def get_coordinates(self, address_query: str):
        # Assign variable for data returned from query.
        # [0] - 1st element in query in the event more than one result returned.
        # ['geometry']['location'] - Target data body.
        geocoded_data = self._google_map_connection.geocode(
            address_query
        )[0]['geometry']['location']

        # Return required data.
        return [
            geocoded_data['lng'],
            geocoded_data['lat']
        ]
