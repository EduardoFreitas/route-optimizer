import unittest
from collections import Counter

from optimizer.location import Location
from optimizer.optimize import Optimize, call_closest_location


class TestOptimize(unittest.TestCase):

    def assert_route_invariants(self, original, ordered):
        self.assertEqual(len(ordered), len(original))
        self.assertEqual(Counter(map(id, ordered)), Counter(map(id, original)))
        if original:
            self.assertIs(ordered[0], original[0])
            self.assertIs(ordered[-1], original[-1])

    def test_empty_route(self):
        optimizer = Optimize([])
        self.assertEqual(optimizer.locations_ordered, [])
        optimizer.calculate()
        self.assertEqual(optimizer.locations_ordered, [])

    def test_single_stop_is_not_duplicated(self):
        location = Location(0, 0, "Only")
        ordered = Optimize([location]).locations_ordered
        self.assertEqual(ordered, [location])
        self.assert_route_invariants([location], ordered)

    def test_two_stops_keep_their_order(self):
        locations = [Location(0, 1, "Start"), Location(0, 0, "End")]
        ordered = Optimize(locations).locations_ordered
        self.assertEqual(ordered, locations)
        self.assert_route_invariants(locations, ordered)

    def test_odd_and_even_route_lengths(self):
        for longitudes in ([0, 2, 1, 3], [0, 3, 1, 2, 4], [0, 4, 1, 3, 2, 5]):
            locations = [
                Location(0, longitude, str(longitude)) for longitude in longitudes
            ]
            with self.subTest(longitudes=longitudes):
                ordered = Optimize(locations).locations_ordered
                self.assert_route_invariants(locations, ordered)
                self.assertEqual(
                    [location.location.longitude for location in ordered],
                    sorted(longitudes),
                )

    def test_input_order_is_not_modified(self):
        locations = [
            Location(0, 0, "Start"),
            Location(0, 3, "Far"),
            Location(0, 1, "Near"),
            Location(0, 4, "End"),
        ]
        original = locations[:]
        optimizer = Optimize(locations)
        self.assertEqual(locations, original)
        self.assertEqual(optimizer.locations, original)
        self.assertIsNot(optimizer.locations, locations)

    def test_recalculation_is_repeatable(self):
        locations = [Location(0, index, str(index)) for index in (0, 3, 1, 2, 4)]
        optimizer = Optimize(locations)
        expected = optimizer.locations_ordered[:]
        optimizer.calculate()
        self.assertEqual(optimizer.locations_ordered, expected)

    def test_duplicate_coordinates_are_preserved(self):
        locations = [
            Location(0, 0, "Start"),
            Location(0, 1, "First visit"),
            Location(0, 1, "Second visit"),
            Location(0, 2, "End"),
        ]
        self.assert_route_invariants(locations, Optimize(locations).locations_ordered)

    def test_repeated_references_are_preserved(self):
        repeated = Location(0, 1, "Repeated")
        locations = [
            Location(0, 0, "Start"), repeated, repeated,
            Location(0, 2, "End"),
        ]
        self.assert_route_invariants(locations, Optimize(locations).locations_ordered)

    def test_return_to_start_preserves_both_endpoint_visits(self):
        start = Location(0, 0, "Start and end")
        locations = [start, Location(0, 2, "Far"), Location(0, 1, "Near"), start]
        self.assert_route_invariants(locations, Optimize(locations).locations_ordered)

    def test_tuple_and_generator_inputs(self):
        locations = [Location(0, index, str(index)) for index in (0, 2, 1, 3)]
        for iterable in (tuple(locations), iter(locations)):
            with self.subTest(iterable=type(iterable).__name__):
                self.assert_route_invariants(
                    locations, Optimize(iterable).locations_ordered
                )

    def test_invalid_route_members_are_rejected(self):
        for value in (None, "a stop", PointLike()):
            with self.subTest(value=value):
                with self.assertRaisesRegex(TypeError, r"locations\[1\]"):
                    Optimize([Location(0, 0, "Start"), value])

    def test_non_iterable_route_is_rejected(self):
        with self.assertRaises(TypeError):
            Optimize(None)


class PointLike:
    latitude = 0
    longitude = 0


class TestClosestLocation(unittest.TestCase):

    def test_empty_candidates(self):
        self.assertEqual(call_closest_location(Location(0, 0, "Start"), []), -1)

    def test_nearest_candidate_index(self):
        start = Location(0, 0, "Start")
        candidates = [Location(0, 3, "Far"), Location(0, 1, "Near")]
        self.assertEqual(call_closest_location(start, candidates), 1)

    def test_ties_choose_the_first_candidate(self):
        start = Location(0, 0, "Start")
        candidates = [Location(0, -1, "First"), Location(0, 1, "Second")]
        self.assertEqual(call_closest_location(start, candidates), 0)


if __name__ == "__main__":
    unittest.main()
