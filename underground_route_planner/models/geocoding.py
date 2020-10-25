import googlemaps
from django.db import models


class GeoCoding:
    def __init__(self):
        # Define internal variable for google map connection.
        self._google_map_connection = googlemaps.Client(
            key='AIzaSyB2JJaU3ySjHvqyO7a_HGNf3-pS0dZBjo4'
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
