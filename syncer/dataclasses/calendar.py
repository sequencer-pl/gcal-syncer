from dataclasses import dataclass
from datetime import datetime

from syncer.formats import GOOGLE_CALENDAR_ALL_DAY_EVENT_DATE


@dataclass(frozen=True)
class Event:
    start: datetime
    end: datetime

    @classmethod
    def parse_from_google_calendar_item(cls, calendar_item: dict):
        return cls(
            start=datetime.strptime(calendar_item['start'].get('date'), GOOGLE_CALENDAR_ALL_DAY_EVENT_DATE),
            end=datetime.strptime(calendar_item['end'].get('date'), GOOGLE_CALENDAR_ALL_DAY_EVENT_DATE),
        )
