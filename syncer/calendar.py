import logging
import os.path
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from syncer.dataclasses.calendar import Event
from syncer.formats import GOOGLE_CALENDAR_DATETIME_FORMAT, GOOGLE_CALENDAR_ALL_DAY_EVENT_DATE, \
    GOOGLE_CALENDAR_DATETIME_TOKEN_JSON_FORMAT

logger = logging.getLogger(__name__)


class Calendar:
    def __init__(self, scopes, token_data=None):
        self.scopes = scopes
        self.credentials = self.get_credentials_from_token_json(token_data) if token_data else self.get_credentials()

    @staticmethod
    def get_credentials_from_token_json(token_data: dict) -> Credentials:
        return Credentials(
            token=token_data['token'],
            refresh_token=token_data['refresh_token'],
            token_uri=token_data['token_uri'],
            client_id=token_data['client_id'],
            client_secret=token_data['client_secret'],
            scopes=token_data['scopes'],
            expiry=datetime.strptime(token_data['expiry'], GOOGLE_CALENDAR_DATETIME_TOKEN_JSON_FORMAT)
        )

    def get_credentials(self) -> Credentials:
        """
        The file token.json stores the user's access and refresh tokens, and is
        created automatically when the authorization flow completes for the first
        time.

        If there are no (valid) credentials available, let the user log in.

        At the end save the credentials for the next run and return user credentials
        """
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scopes)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w', encoding='utf8') as token:
                token.write(creds.to_json())
        return creds

    def get_items(self, calendar_id: str, days: int) -> list[Event]:
        service = build('calendar', 'v3', credentials=self.credentials)
        _from = datetime.today()
        _to = _from + timedelta(days=days)
        logger.info('Getting upcoming events for the next %s days', days)
        events_result = service.events().list(  # pylint: disable=maybe-no-member
            calendarId=calendar_id,
            timeMin=_from.strftime(GOOGLE_CALENDAR_DATETIME_FORMAT),
            timeMax=_to.strftime(GOOGLE_CALENDAR_DATETIME_FORMAT),
            maxResults=99_999,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        return [Event(
            item_id=e['id'],
            start=datetime.strptime(e['start'].get('date'), GOOGLE_CALENDAR_ALL_DAY_EVENT_DATE),
            end=datetime.strptime(e['end'].get('date'), GOOGLE_CALENDAR_ALL_DAY_EVENT_DATE),
        ) for e in self._get_all_day_events_only(events_result.get('items', []))]

    @staticmethod
    def _get_all_day_events_only(events):
        return [e for e in events if e['start'].get('date') and e['end'].get('date')]

    def add_items(self, calendar_id: str, items: list[Event], description) -> None:
        service = build('calendar', 'v3', credentials=self.credentials)
        for item in items:
            event = {
                'summary': description,
                'start': {
                    'date': item.start.strftime(GOOGLE_CALENDAR_ALL_DAY_EVENT_DATE)
                },
                'end': {
                    'date': item.end.strftime(GOOGLE_CALENDAR_ALL_DAY_EVENT_DATE)
                }
            }
            service.events().insert(calendarId=calendar_id, body=event).execute()  # pylint: disable=maybe-no-member

    def delete_items(self, calendar_id: str, items: list[Event]) -> None:
        service = build('calendar', 'v3', credentials=self.credentials)
        for item in items:
            service.events().delete(  # pylint: disable=maybe-no-member
                calendarId=calendar_id, eventId=item.item_id
            ).execute()
