from numbers import Real


class Point:

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def _validate_coordinate(value, name, limit):
        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError("{} must be a real number".format(name))
        if not -limit <= value <= limit:
            raise ValueError(
                "{} must be finite and between {} and {}".format(name, -limit, limit)
            )
        return value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        self._latitude = self._validate_coordinate(value, "latitude", 90)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        self._longitude = self._validate_coordinate(value, "longitude", 180)
