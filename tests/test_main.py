from unittest import TestCase
from unittest.mock import patch, call

from syncer.main import sync


class MainTest(TestCase):
    @patch("syncer.main.Calendar")
    def test_sync_executes_get_and_compare_events(self, m_calendar):
        cal = m_calendar()

        sync('src_cal_id', 'dst_cal_id', True, 'Description', 13, token_data={})

        cal.get_items.assert_has_calls([
            call('src_cal_id', 13),
            call('dst_cal_id', 13),
        ])

