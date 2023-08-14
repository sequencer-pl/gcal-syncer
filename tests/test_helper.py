from datetime import datetime
from unittest import TestCase

from syncer.dataclasses.calendar import Event
from syncer.helper import compare_events_lists


class HelperTest(TestCase):
    def setUp(self) -> None:
        self.events1 = {
            Event(
                start=datetime(year=1985, month=10, day=26),
                end=datetime(year=1985, month=10, day=26),
            ),
            Event(
                start=datetime(year=1955, month=11, day=5),
                end=datetime(year=1955, month=11, day=12),
            ),
            Event(
                start=datetime(year=2015, month=10, day=21),
                end=datetime(year=2015, month=10, day=21),
            ),
        }
        self.events2 = {
            Event(
                start=datetime(year=2015, month=10, day=21),
                end=datetime(year=2015, month=10, day=21),
            ),
            Event(
                start=datetime(year=1, month=1, day=1),
                end=datetime(year=1, month=1, day=1),
            ),
        }

    def test_compare_events_returns_tuple_with_events_to_add_and_to_remove(self):
        expected_to_add = {
            Event(
                start=datetime(year=1985, month=10, day=26),
                end=datetime(year=1985, month=10, day=26),
            ),
            Event(
                start=datetime(year=1955, month=11, day=5),
                end=datetime(year=1955, month=11, day=12),
            )
        }
        expected_to_delete = {
            Event(
                start=datetime(year=1, month=1, day=1),
                end=datetime(year=1, month=1, day=1),
            )
        }

        to_add, to_delete = compare_events_lists(self.events1, self.events2)

        self.assertSetEqual(to_add, expected_to_add)
        self.assertSetEqual(to_delete, expected_to_delete)
