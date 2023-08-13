from dataclasses import dataclass
from datetime import datetime

from syncer.formats import GOOGLE_CALENDAR_ALL_DAY_EVENT_DATE


@dataclass
class Event:
    start: datetime
    end: datetime
    status: str

    @classmethod
    def parse_from_google_calendar_item(cls, calendar_item: dict):
        return cls(
            start=datetime.strptime(calendar_item['start'].get('date'), GOOGLE_CALENDAR_ALL_DAY_EVENT_DATE),
            end=datetime.strptime(calendar_item['end'].get('date'), GOOGLE_CALENDAR_ALL_DAY_EVENT_DATE),
            status=calendar_item.get('status', 'confirmed')
        )
