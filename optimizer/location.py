from optimizer.point import Point
import math


class Location(object):

    def __init__(self, latitude, longitude, name):
        self.location = Point(latitude, longitude)
        self.name = name

    def calculate_distance(self, city):
        return 102960 * math.sqrt(math.pow((self.location.longitude - city.location.longitude), 2) + math.pow(
            (self.location.latitude - city.location.latitude), 2))

    def __str__(self):
        return "Name: {} Object Location:{}, {}".format(self.name, self.location.latitude, self.location.longitude)