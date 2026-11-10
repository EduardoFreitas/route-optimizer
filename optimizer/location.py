import math

from optimizer.point import Point


EARTH_RADIUS_METERS = 6_371_008.8


class Location(object):

    def __init__(self, latitude, longitude, name):
        self.location = Point(latitude, longitude)
        self.name = name

    def calculate_distance(self, city):
        """Return the spherical great-circle distance to another Location, in meters."""
        if not isinstance(city, Location):
            raise TypeError("city must be a Location")

        latitude = math.radians(self.location.latitude)
        other_latitude = math.radians(city.location.latitude)
        latitude_difference = other_latitude - latitude
        longitude_difference = math.radians(
            city.location.longitude - self.location.longitude
        )
        haversine = (
            math.sin(latitude_difference / 2) ** 2
            + math.cos(latitude)
            * math.cos(other_latitude)
            * math.sin(longitude_difference / 2) ** 2
        )
        # Rounding near antipodal points can put the value just outside [0, 1].
        haversine = min(1.0, max(0.0, haversine))
        return 2 * EARTH_RADIUS_METERS * math.atan2(
            math.sqrt(haversine), math.sqrt(1 - haversine)
        )

    def __str__(self):
        return "Name: {} Object Location:{}, {}".format(self.name, self.location.latitude, self.location.longitude)