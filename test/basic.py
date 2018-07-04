from optimizer.location import Location
from optimizer.optimize import Optimize

if __name__ == '__main__':
    cities = []
    cities.append(Location(-25.457010, -49.239443, "Start"))
    cities.append(Location(-25.404969, -49.265481, "Stop 1"))
    cities.append(Location(-25.415049, -49.244710, "Stop 2"))
    cities.append(Location(-25.431562, -49.236041, "Stop 3"))
    cities.append(Location(-25.433817, -49.278323, "End"))

    optimize = Optimize(cities)

    for c in cities:
        print(c)
    print("--------------")
    for c in optimize.locations_ordered:
        print(c)
