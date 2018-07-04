import sys


class Optimize(object):

    def __init__(self, locations):
        self.locations = locations
        self.locations_ordered = []
        self.calculate()

    def calculate(self):
        forward_arrange = []
        reverse_arrange = []

        # separate from array
        forward_arrange.append(self.locations[0])
        reverse_arrange.append(self.locations[-1])

        # remove start and end
        arrange = self.locations[1:len(self.locations)-1]

        while True:
            location_closest = call_closest_location(forward_arrange[-1], arrange)
            if location_closest > -1:
                forward_arrange.append(arrange[location_closest])
                arrange.pop(location_closest)
            if len(arrange) == 0:
                break
            location_closest = call_closest_location(reverse_arrange[-1], arrange)
            if location_closest > -1:
                reverse_arrange.append(arrange[location_closest])
                arrange.pop(location_closest)
            if len(arrange) < 0:
                break

        self.locations_ordered = forward_arrange + list(reversed(reverse_arrange))


def call_closest_location(city, cities):
    if len(cities) == 0:
        return -1
    distance = sys.float_info.max
    for city_array in cities:
        actual_distance = (city.calculate_distance(city_array))
        if actual_distance < distance:
            distance = actual_distance
            index = cities.index(city_array)

    return index
