from __future__ import annotations

import unittest
from copy import deepcopy
from typing import TYPE_CHECKING

import itertools as it

import jinete as jit

from tests.utils import (
    generate_routes,
)

if TYPE_CHECKING:
    from typing import (
        Set,
        List
    )


class TestPlanning(unittest.TestCase):
    routes: Set[jit.Route]
    loaded_routes: Set[jit.Route]
    planned_trips: List[jit.PlannedTrip]
    trips: List[jit.Trip]

    @classmethod
    def setUpClass(cls) -> None:
        cls.routes = generate_routes(3)
        cls.loaded_routes = set(route for route in cls.routes if route.loaded)
        cls.planned_trips = list(it.chain.from_iterable(route.planned_trips for route in cls.routes))
        cls.trips = list(planned_trip.trip for planned_trip in cls.planned_trips)

    def test_construction(self):
        planning = jit.Planning(self.routes)

        self.assertIsInstance(planning, jit.Planning)
        self.assertEqual(planning.routes, self.routes)
        self.assertEqual(planning.loaded_routes, self.loaded_routes)
        self.assertEqual(list(planning.planned_trips), self.planned_trips)
        self.assertEqual(list(planning.trips), self.trips)

    def test_deepcopy(self):
        planning = jit.Planning(self.routes)

        copied_planning = deepcopy(planning)
        self.assertNotEqual(planning, copied_planning)
        self.assertNotEqual(id(planning), id(copied_planning))
        self.assertNotEqual(planning.uuid, copied_planning.uuid)
        self.assertEqual(len(planning.routes), len(copied_planning.routes))
        self.assertTrue(planning.routes.isdisjoint(copied_planning.routes))
        for route in planning.routes:
            assert any(set(route.trips).isdisjoint(copied_route.trips) for copied_route in copied_planning)


if __name__ == '__main__':
    unittest.main()
