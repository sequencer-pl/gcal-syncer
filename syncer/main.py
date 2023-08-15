import json
import logging

import click

from syncer.calendar import Calendar
from syncer.helper import compare_events_lists
from syncer.logger import logging_setup

logger = logging.getLogger(__name__)


@click.command()
@click.option('-s', '--source_calendar_id', required=True,
              help='A calendar identifier from data will be copied. Example: abc@group.calendar.google.com')
@click.option('-d', '--destination_calendar_id', required=True,
              help='The identifier of a calendar to which data will be copied. Example: abc@group.calendar.google.com')
@click.option('-a', '--all-day-only', is_flag=True, default=True,
              help="At the moment it allows sync only all day events. This flag is always true.")
@click.option('-e', '--events_description', default='Free time!',
              help='Description for added events')
@click.option('-n', '--number_of_days_to_sync', type=int, default=365,
              help='How many days from today do you want to synchronize')
@click.option('-t', '--token_json', default='{}',
              help='Token json content. Paste it in apostrophes, E.g. \'{"token": "Lorem..."}...\'')
def run(
        source_calendar_id: str,
        destination_calendar_id: str,
        all_day_only: bool,
        events_description: str,
        number_of_days_to_sync: int,
        token_json: str
) -> None:
    """Small description"""
    logging_setup()
    token_data = json.loads(token_json)
    sync(
        source_calendar_id,
        destination_calendar_id,
        all_day_only, events_description,
        number_of_days_to_sync,
        token_data
    )


def sync(
        source_calendar_id: str,
        destination_calendar_id: str,
        all_day_only: bool,
        events_description: str,
        number_of_days_to_sync: int,
        token_data: str
):
    calendar = Calendar(scopes=['https://www.googleapis.com/auth/calendar.events'], token_data=token_data)
    src_events = calendar.get_items(source_calendar_id, number_of_days_to_sync)
    dst_events = calendar.get_items(destination_calendar_id, number_of_days_to_sync)
    events_to_add, events_to_remove = compare_events_lists(src_events, dst_events)
    logger.info("Events to remove: %s", events_to_remove)
    calendar.delete_items(destination_calendar_id, events_to_remove)
    logger.info("Events to add: %s", events_to_add)
    calendar.add_items(destination_calendar_id, events_to_add, events_description)
    logger.info("%s days synced successfully", number_of_days_to_sync)
    _ = all_day_only  # sync not only all day events
