from city import City
from optimize import Optimize

if __name__ == '__main__':

    start = City(-25.457010, -49.239443, "Start")
    stop1 = City(-25.404969, -49.265481, "Stop 1")
    stop2 = City(-25.415049, -49.244710, "Stop 2")
    stop3 = City(-25.431562, -49.236041, "Stop 3")
    end = City(-25.433817, -49.278323, "End")

    cities = []
    cities.append(start)
    cities.append(stop1)
    cities.append(stop2)
    cities.append(stop3)
    cities.append(end)

    cities_ordered = Optimize(cities).calculate()

    for c in cities:
        print(c)
    print("--------------")
    for c in cities_ordered:
        print(c)
