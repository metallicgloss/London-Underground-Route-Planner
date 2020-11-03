import googlemaps
from django.db import models


class GeoCoding:
    def __init__(self, route_geocoding_api_key):
        # Define internal variable for google map connection.
        self._google_map_connection = googlemaps.Client(
            key=route_geocoding_api_key
        )

    def get_coordinates(self, address_query: str):
        # Return coordinates for address query.

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
