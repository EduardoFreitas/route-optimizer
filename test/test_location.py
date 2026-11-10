import math
import unittest

from optimizer.location import EARTH_RADIUS_METERS, Location
from optimizer.point import Point


class TestPoint(unittest.TestCase):

    def test_coordinate_boundaries(self):
        for latitude in (-90, 0, 90):
            for longitude in (-180, 0, 180):
                with self.subTest(latitude=latitude, longitude=longitude):
                    point = Point(latitude, longitude)
                    self.assertEqual(point.latitude, latitude)
                    self.assertEqual(point.longitude, longitude)

    def test_coordinate_types(self):
        for name in ("latitude", "longitude"):
            for value in (None, "0", True, False, 1j, []):
                coordinates = {"latitude": 0, "longitude": 0}
                coordinates[name] = value
                with self.subTest(name=name, value=value):
                    with self.assertRaisesRegex(TypeError, name):
                        Point(**coordinates)

    def test_coordinate_ranges_and_finiteness(self):
        for name, limit in (("latitude", 90), ("longitude", 180)):
            for value in (
                -limit - 0.001, limit + 0.001,
                float("nan"), float("inf"), -float("inf"), 10 ** 400,
            ):
                coordinates = {"latitude": 0, "longitude": 0}
                coordinates[name] = value
                with self.subTest(name=name, value=value):
                    with self.assertRaisesRegex(ValueError, name):
                        Point(**coordinates)

    def test_valid_coordinate_updates(self):
        point = Point(0, 0)
        point.latitude = 45.5
        point.longitude = -120.25
        self.assertEqual(point.latitude, 45.5)
        self.assertEqual(point.longitude, -120.25)

    def test_invalid_coordinate_updates_preserve_previous_value(self):
        point = Point(10, 20)
        for name, value, error in (
            ("latitude", 91, ValueError),
            ("longitude", -181, ValueError),
            ("latitude", float("nan"), ValueError),
            ("longitude", "20", TypeError),
        ):
            previous = getattr(point, name)
            with self.subTest(name=name, value=value):
                with self.assertRaises(error):
                    setattr(point, name, value)
                self.assertEqual(getattr(point, name), previous)


class TestLocation(unittest.TestCase):

    def test_identical_coordinates_have_zero_distance(self):
        first = Location(-25.45, -49.23, "First")
        second = Location(-25.45, -49.23, "Second")
        self.assertEqual(first.calculate_distance(first), 0)
        self.assertEqual(first.calculate_distance(second), 0)

    def test_one_equatorial_degree_in_meters(self):
        origin = Location(0, 0, "Origin")
        destination = Location(0, 1, "Destination")
        self.assertAlmostEqual(
            origin.calculate_distance(destination), 111_195.080234, delta=0.01
        )

    def test_london_to_new_york(self):
        london = Location(51.5074, -0.1278, "London")
        new_york = Location(40.7128, -74.0060, "New York")
        self.assertAlmostEqual(
            london.calculate_distance(new_york), 5_570_230, delta=100
        )

    def test_distance_is_symmetric(self):
        first = Location(-25.45, -49.23, "First")
        second = Location(49.88, -119.50, "Second")
        self.assertAlmostEqual(
            first.calculate_distance(second), second.calculate_distance(first),
            delta=0.000001,
        )

    def test_crossing_the_date_line_takes_the_short_arc(self):
        first = Location(0, 179.9, "West")
        second = Location(0, -179.9, "East")
        self.assertAlmostEqual(
            first.calculate_distance(second), 22_239.016047, delta=0.01
        )

    def test_longitude_distances_shrink_near_the_pole(self):
        first = Location(89, 0, "First")
        second = Location(89, 90, "Second")
        self.assertGreater(first.calculate_distance(second), 150_000)
        self.assertLess(first.calculate_distance(second), 160_000)

    def test_longitudes_at_the_same_pole_are_coincident(self):
        first = Location(90, -180, "First")
        second = Location(90, 180, "Second")
        self.assertAlmostEqual(first.calculate_distance(second), 0, delta=0.000001)

    def test_antipodal_distance(self):
        first = Location(0, 0, "First")
        second = Location(0, 180, "Second")
        self.assertAlmostEqual(
            first.calculate_distance(second),
            math.pi * EARTH_RADIUS_METERS,
            delta=0.000001,
        )

    def test_nearly_antipodal_distance_is_finite(self):
        first = Location(23.4567, 45.6789, "First")
        second = Location(-23.4567, -134.3210999, "Second")
        distance = first.calculate_distance(second)
        self.assertTrue(math.isfinite(distance))
        self.assertAlmostEqual(
            distance, math.pi * EARTH_RADIUS_METERS, delta=1
        )

    def test_non_location_destination_is_rejected(self):
        with self.assertRaisesRegex(TypeError, "Location"):
            Location(0, 0, "Origin").calculate_distance(None)


if __name__ == "__main__":
    unittest.main()
