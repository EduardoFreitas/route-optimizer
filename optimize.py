import sys


class Optimize(object):

    def __init__(self, cities):
        self.cities = cities

    def calculate(self):
        arrange = []
        forward_arrange = []
        reverse_arrange = []

        # separete from array
        start = self.cities[0]
        end = self.cities[-1]
        # remove start and end
        for x in range(len(self.cities) - 2):
            arrange.append(self.cities[x + 1])

        while True:
            city_closest = self.call_closest_location(start, arrange)
            forward_arrange.append(start)
            if city_closest > -1:
                forward_arrange.append(arrange[city_closest])
                arrange.pop(city_closest)
            if len(arrange) == 0:
                break
            city_closest = self.call_closest_location(end, arrange)
            reverse_arrange.append(end)
            if city_closest > -1:
                reverse_arrange.append(arrange[city_closest])
                arrange.pop(city_closest)
            if len(arrange) > 0:
                start = arrange[0]
                arrange.pop(0)
            else:
                break
            if len(arrange) > 0:
                end = arrange[-1]
                arrange.pop(-1)

        return forward_arrange + list(reversed(reverse_arrange))

    def call_closest_location(self, city, cities):
        if len(cities) == 0:
            return -1
        distance = sys.float_info.max
        for city_array in cities:
            actual_distance = (city.calculate_distance(city_array))
            if actual_distance < distance:
                distance = actual_distance
                index = cities.index(city_array)

        return index
