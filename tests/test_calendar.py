import datetime
from unittest import TestCase
from unittest.mock import patch, MagicMock

import freezegun

from syncer.calendar import Calendar
from syncer.dataclasses.calendar import Event
from syncer.formats import GOOGLE_CALENDAR_ALL_DAY_EVENT_DATE


class CalendarCredentialsTest(TestCase):

    @patch("syncer.calendar.Credentials")
    @patch('syncer.calendar.os')
    def test_check_credentials_get_credentials_with_scope_from_token_json_if_token_file_exists(
            self, m_os, m_credentials
    ):
        scopes = ['test.scope.calendar']
        m_os.path.exists.return_value = True

        Calendar(scopes)

        m_credentials.from_authorized_user_file.assert_called_once_with('token.json', scopes)


class CalendarTest(TestCase):
    @patch('syncer.calendar.Calendar.get_credentials')
    def setUp(self, _) -> None:
        self.scopes = ['test.scope.calendar']
        self.calendar_id = 'test@cal.id'
        self.calendar = Calendar(
            scopes=self.scopes
        )

    def tearDown(self) -> None:
        pass

    @patch("syncer.calendar.build")
    def test_get_calendar_items_executes_google_api_service_events_list_request(
            self, m_build
    ):
        m_events = m_build().events.return_value = MagicMock()
        sync_days = 300
        start = datetime.datetime(year=1985, month=10, day=26, hour=1, minute=22)
        end = start + datetime.timedelta(days=sync_days)

        with freezegun.freeze_time(start):
            self.calendar.get_calendar_items('test@cal.id', sync_days)

        m_events.list.assert_called_once_with(
            calendarId=self.calendar_id,
            timeMin=start.strftime(GOOGLE_CALENDAR_ALL_DAY_EVENT_DATE),
            timeMax=end.strftime(GOOGLE_CALENDAR_ALL_DAY_EVENT_DATE),
            maxResults=99999,
            singleEvents=True,
            orderBy='startTime',
        )

    @patch("syncer.calendar.build")
    def test_get_calendar_items_returns_list_of_events_objects(self, m_build):
        m_events = m_build().events.return_value = MagicMock()
        m_list = m_events.list.return_value = MagicMock()
        event = {
            'start': {'date': '1955-11-05'},
            'end': {'date': '1955-11-05'},
            'status': 'confirmed'
        }
        m_list.execute.return_value = {'items': [event]}
        expected_event = Event(
            start=datetime.datetime(year=1955, month=11, day=5),
            end=datetime.datetime(year=1955, month=11, day=5),
        )

        events = self.calendar.get_calendar_items(calendar_id=self.calendar_id, days=3)

        self.assertListEqual(events, [expected_event])

    @patch("syncer.calendar.build")
    def test_get_calendar_items_returns_all_day_events_only(self, m_build):
        m_events = m_build().events.return_value = MagicMock()
        m_list = m_events.list.return_value = MagicMock()
        all_day_event = {
            'start': {'date': '1955-11-05'},
            'end': {'date': '1955-11-05'},
            'status': 'confirmed'
        }
        part_day_event = {
            'start': {'dateTime': '2023-08-14T09:37:00+02:00', 'timeZone': 'Europe/Warsaw'},
            'end': {'dateTime': '2023-08-14T12:37:00+02:00', 'timeZone': 'Europe/Warsaw'},
            'status': 'confirmed'
        }
        m_list.execute.return_value = {'items': [all_day_event, part_day_event]}
        expected_event = Event.parse_from_google_calendar_item(all_day_event)

        events = self.calendar.get_calendar_items('', 2)

        self.assertListEqual(events, [expected_event])
