from datetime import datetime, timedelta
from unittest import TestCase
from unittest.mock import patch, MagicMock, call

import freezegun

from syncer.calendar import Calendar
from syncer.dataclasses.calendar import Event
from syncer.formats import GOOGLE_CALENDAR_DATETIME_FORMAT


class CalendarCredentialsTest(TestCase):

    @patch("syncer.calendar.Credentials")
    @patch('syncer.calendar.os')
    def test_get_credentials_with_scope_from_token_json_if_token_file_exists(
            self, m_os, m_credentials
    ):
        scopes = ['test.scope.calendar']
        m_os.path.exists.return_value = True

        Calendar(scopes)

        m_credentials.from_authorized_user_file.assert_called_once_with('token.json', scopes)


@patch("syncer.calendar.build")
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

    def test_get_items_executes_google_api_service_events_list_request(
            self, m_build
    ):
        m_events = m_build().events.return_value = MagicMock()
        sync_days = 300
        start = datetime(year=1985, month=10, day=26, hour=1, minute=22)
        end = start + timedelta(days=sync_days)

        with freezegun.freeze_time(start):
            self.calendar.get_items('test@cal.id', sync_days)

        m_events.list.assert_called_once_with(
            calendarId=self.calendar_id,
            timeMin=start.strftime(GOOGLE_CALENDAR_DATETIME_FORMAT),
            timeMax=end.strftime(GOOGLE_CALENDAR_DATETIME_FORMAT),
            maxResults=99999,
            singleEvents=True,
            orderBy='startTime',
        )

    def test_get_items_returns_list_of_events_objects(self, m_build):
        m_events = m_build().events.return_value = MagicMock()
        m_list = m_events.list.return_value = MagicMock()
        event = {
            'id': 'id1',
            'start': {'date': '1955-11-05'},
            'end': {'date': '1955-11-05'},
        }
        m_list.execute.return_value = {'items': [event]}
        expected_event = Event(
            item_id='id1',
            start=datetime(year=1955, month=11, day=5),
            end=datetime(year=1955, month=11, day=5),
        )

        events = self.calendar.get_items(calendar_id=self.calendar_id, days=3)

        self.assertListEqual(events, [expected_event])

    def test_get_items_returns_all_day_events_only(self, m_build):
        m_events = m_build().events.return_value = MagicMock()
        m_list = m_events.list.return_value = MagicMock()
        all_day_event = {
            'id': 'id1',
            'start': {'date': '1955-11-05'},
            'end': {'date': '1955-11-05'},
        }
        part_day_event = {
            'id': 'id2',
            'start': {'dateTime': '2023-08-14T09:37:00+02:00', 'timeZone': 'Europe/Warsaw'},
            'end': {'dateTime': '2023-08-14T12:37:00+02:00', 'timeZone': 'Europe/Warsaw'},
        }
        m_list.execute.return_value = {'items': [all_day_event, part_day_event]}
        expected_event = Event.parse_from_google_calendar_item(all_day_event)

        events = self.calendar.get_items('', 2)

        self.assertListEqual(events, [expected_event])

    def test_add_items_execute_events_insert_with_proper_params(self, m_build):
        m_events = m_build().events.return_value = MagicMock()
        events = [
            Event(item_id='id1', start=datetime(year=1985, month=10, day=26), end=datetime(year=1985, month=10, day=26)),
            Event(item_id='id2', start=datetime(year=1985, month=11, day=26), end=datetime(year=1985, month=12, day=26)),
        ]
        dst_cal_id = 'cal@id'

        self.calendar.add_items(calendar_id=dst_cal_id, items=events, description='Description')

        m_events.insert.assert_has_calls([
            call(calendarId=dst_cal_id, body={
                'summary': 'Description',
                'start': {
                    'date': '1985-10-26'
                },
                'end': {
                    'date': '1985-10-26'
                }
            }),
            call().execute(),
            call(calendarId=dst_cal_id, body={
                'summary': 'Description',
                'start': {
                    'date': '1985-11-26'
                },
                'end': {
                    'date': '1985-12-26'
                }
            }),
            call().execute()
        ])

    def test_delete_items_execute_events_delete_with_correct_event_id(self, m_build):
        m_events = m_build().events.return_value = MagicMock()
        events = [
            Event(item_id='id1', start=datetime(year=1985, month=10, day=26), end=datetime(year=1985, month=10, day=26)),
            Event(item_id='id2', start=datetime(year=1985, month=11, day=26), end=datetime(year=1985, month=12, day=26)),
        ]
        dst_cal_id = 'cal@id'

        self.calendar.delete_items(calendar_id=dst_cal_id, items=events)

        m_events.delete.assert_has_calls([
            call(calendarId=dst_cal_id, eventId=events[0].item_id),
            call().execute(),
            call(calendarId=dst_cal_id, eventId=events[1].item_id),
            call().execute(),
        ])
