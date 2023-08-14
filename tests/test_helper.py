from datetime import datetime
from unittest import TestCase

from syncer.dataclasses.calendar import Event
from syncer.helper import compare_events_lists


class HelperTest(TestCase):
    def setUp(self) -> None:
        self.events1 = [
            Event(
                item_id='OneDayEventToAdd',
                start=datetime(year=1985, month=10, day=26),
                end=datetime(year=1985, month=10, day=26),
            ),
            Event(
                item_id='WeekEventToAdd',
                start=datetime(year=1955, month=11, day=5),
                end=datetime(year=1955, month=11, day=12),
            ),
            Event(
                item_id='ToKeepFromFirstCalendar',
                start=datetime(year=2015, month=10, day=21),
                end=datetime(year=2015, month=10, day=21),
            ),
        ]
        self.events2 = [
            Event(
                item_id='ToKeepFromSecondCalendar',
                start=datetime(year=2015, month=10, day=21),
                end=datetime(year=2015, month=10, day=21),
            ),
            Event(
                item_id='ToDelete',
                start=datetime(year=1, month=1, day=1),
                end=datetime(year=1, month=1, day=1),
            ),
        ]

    def test_compare_events_returns_tuple_with_events_to_add_and_to_remove(self):
        expected_to_add = [
            Event(
                item_id='OneDayEventToAdd',
                start=datetime(year=1985, month=10, day=26),
                end=datetime(year=1985, month=10, day=26),
            ),
            Event(
                item_id='WeekEventToAdd',
                start=datetime(year=1955, month=11, day=5),
                end=datetime(year=1955, month=11, day=12),
            )
        ]
        expected_to_delete = [
            Event(
                item_id='ToDelete',
                start=datetime(year=1, month=1, day=1),
                end=datetime(year=1, month=1, day=1),
            )
        ]

        to_add, to_delete = compare_events_lists(self.events1, self.events2)

        self.assertListEqual(to_add, expected_to_add)
        self.assertListEqual(to_delete, expected_to_delete)
