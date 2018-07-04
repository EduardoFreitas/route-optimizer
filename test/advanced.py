import json
import random
import simplekml

from optimizer.location import Location
from optimizer.optimize import Optimize


def scrambled(orig):
    dest = orig[:]
    random.shuffle(dest)
    return dest


# {
#   "codigo_ibge": 4103909,
#   "nome_municipio": "Campina da Lagoa",
#   "capital": false,
#   "codigo_uf": 41,
#   "uf": "PR",
#   "estado": "Paraná",
#   "latitude": -24.5893,
#   "longitude": -52.7976
# }
if __name__ == '__main__':

    kml = simplekml.Kml()

    with open('data.json', encoding="utf8") as f:
        data = json.load(f)

    lowest = {}
    lowest['latitude'] = 180
    highest = {}
    highest['latitude'] = -180

    capitals = []

    for x in data:
        if x['capital']:
            capitals.append(x)
            kml.newpoint(name='{} - {}'.format(x['nome_municipio'], x['uf']), coords=[(x['longitude'], x['latitude'])])
            if x['latitude'] < lowest['latitude']:
                lowest = x
            if x['latitude'] > highest['latitude']:
                highest = x

    capitals.remove(lowest)
    capitals.remove(highest)

    capitals = scrambled(capitals)
    capitals.insert(0, lowest)
    capitals.append(highest)
    cities = []
    for x in capitals:
        cities.append(Location(x['latitude'], x['longitude'], x['uf']))

    optimize = Optimize(cities)

    for c in cities:
        print(c)
    print("--------------")
    newarray = []
    for c in optimize.locations_ordered:
        newarray.append((c.location.longitude, c.location.latitude))
        print(c)
    kml.newlinestring(name="Pathway", description="Best Route", coords=newarray)
    kml.save("optimize.kml")
