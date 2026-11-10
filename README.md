# Route Optimizer

[![Tests](https://github.com/EduardoFreitas/route-optimizer/actions/workflows/tests.yml/badge.svg)](https://github.com/EduardoFreitas/route-optimizer/actions/workflows/tests.yml)

Reorder geographic stops with a lightweight Python heuristic, without calling
Google Maps or another external routing API.

The first and last stops stay fixed. Intermediate stops are added alternately
to the start and end of the route, choosing the nearest remaining stop at each
step.

## Requirements

- Python 3.10 or later.
- No third-party dependencies for the optimizer or unit tests.
- `simplekml` is needed only for the optional KML example.

Clone the repository and run commands from its root:

```shell
git clone https://github.com/EduardoFreitas/route-optimizer.git
cd route-optimizer
```

## Quick start

```python
from optimizer.location import Location
from optimizer.optimize import Optimize

stops = [
    Location(0, 0, "Start"),
    Location(0, 3, "Stop 3"),
    Location(0, 1, "Stop 1"),
    Location(0, 2, "Stop 2"),
    Location(0, 4, "End"),
]

route = Optimize(stops).locations_ordered
distance_meters = sum(
    first.calculate_distance(second)
    for first, second in zip(route, route[1:])
)

print([stop.name for stop in route])
print("{:.2f} meters".format(distance_meters))
```

Output:

```text
['Start', 'Stop 1', 'Stop 2', 'Stop 3', 'End']
444780.32 meters
```

## Distances and limitations

`Location.calculate_distance(other)` returns **meters**, using the Haversine
formula and a mean Earth radius of 6,371,008.8 meters. It measures the shorter
great-circle arc on a sphere, including across the international date line.

- These are geographic distances, **not road distances or travel times**.
- The spherical model approximates the Earth's ellipsoidal shape.
- The optimizer is a greedy heuristic, not an exact traveling-salesperson solver.
  It does not guarantee the shortest route or an improvement over every input
  ordering.
- There is no traffic, road-network, vehicle-capacity, or time-window model.
- Route ordering and reported distances can differ from older versions, which
  used a flat-coordinate distance approximation.

## Input behavior

- Pass an iterable of `Location` objects; lists, tuples, and generators work.
- The input is copied without reordering or modifying the supplied collection.
  The resulting route contains the original `Location` objects.
- An empty route returns `[]`; a single stop appears once; two stops keep their
  original order.
- Every supplied visit is retained, including duplicate coordinates or repeated
  references to the same location.
- For routes with at least two stops, the first and last supplied visits remain
  the endpoints. Repeat the start as the last visit to return to it.
- Ties choose the first candidate in the remaining input order.
- Coordinates must be real numbers, excluding booleans. Latitude must be within
  `[-90, 90]` and longitude within `[-180, 180]`, inclusive.
- Non-numeric coordinates and non-`Location` route members raise `TypeError`.
  Out-of-range and non-finite coordinates raise `ValueError`. Coordinate updates
  through `Point.latitude` and `Point.longitude` are validated too.
- Calling `calculate()` again recomputes the route from the optimizer's copied
  input.

## Examples

Run the original small-route example:

```shell
python -m test.basic
```

To export the included Brazilian-capitals example as KML:

```shell
python -m pip install -r requirements.txt
python -m test.advanced
```

The KML example shuffles the intermediate cities, so its route may vary between
runs. It writes `optimize.kml` in the current working directory. Open it in a
KML-compatible map viewer; the connecting lines do not represent roads.

## Tests

```shell
python -m unittest discover -s test -p "test_*.py" -v
```

Tests cover reference distances, poles, antipodal points, date-line crossings,
coordinate validation, fixed endpoints, duplicate visits, input preservation,
and empty/single-stop routes.

GitHub Actions runs the unit tests and basic example on Windows and Linux with
Python 3.10, 3.12, and 3.14. The optional KML example is also checked on Linux
with Python 3.12.
