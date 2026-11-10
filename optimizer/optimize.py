from optimizer.location import Location


class Optimize(object):

    def __init__(self, locations):
        self.locations = list(locations)
        for index, location in enumerate(self.locations):
            if not isinstance(location, Location):
                raise TypeError("locations[{}] must be a Location".format(index))
        self.locations_ordered = []
        self.calculate()

    def calculate(self):
        if len(self.locations) < 2:
            self.locations_ordered = self.locations[:]
            return

        forward_arrange = [self.locations[0]]
        reverse_arrange = [self.locations[-1]]
        arrange = self.locations[1:-1]

        while arrange:
            location_closest = call_closest_location(forward_arrange[-1], arrange)
            forward_arrange.append(arrange.pop(location_closest))
            if arrange:
                location_closest = call_closest_location(reverse_arrange[-1], arrange)
                reverse_arrange.append(arrange.pop(location_closest))

        self.locations_ordered = forward_arrange + list(reversed(reverse_arrange))


def call_closest_location(city, cities):
    closest_index = -1
    distance = float("inf")
    for index, city_array in enumerate(cities):
        actual_distance = city.calculate_distance(city_array)
        if actual_distance < distance:
            distance = actual_distance
            closest_index = index

    return closest_index
