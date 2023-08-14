"""
MODULE
"""
import click

from syncer.calendar import Calendar
from syncer.helper import compare_events_lists


@click.command()
@click.option('-s', '--source_calendar_id',
              help='A calendar identifier from data will be copied. Example: abc@group.calendar.google.com')
@click.option('-d', '--destination_calendar_id',
              help='The identifier of a calendar to which data will be copied. Example: abc@group.calendar.google.com')
@click.option('-a', '--all-day-only', is_flag=True,
              help="For now, it's only a placeholder. It does not work.")
@click.option('-e', '--events_description',
              help='Description for added events')
@click.option('-n', '--number_of_days_to_sync', type=int,
              help='How many days from today do you want to synchronize')
def run(
        source_calendar_id: str,
        destination_calendar_id: str,
        all_day_only: bool,
        events_description: str,
        number_of_days_to_sync: int
) -> None:
    """SYNC"""
    sync(source_calendar_id, destination_calendar_id, all_day_only, events_description, number_of_days_to_sync)


def sync(
        source_calendar_id: str,
        destination_calendar_id: str,
        all_day_only: bool,
        events_description: str,
        number_of_days_to_sync: int
):
    calendar = Calendar(scopes=['https://www.googleapis.com/auth/calendar.events'])
    src_events = calendar.get_calendar_items(source_calendar_id, number_of_days_to_sync)
    dst_events = calendar.get_calendar_items(destination_calendar_id, number_of_days_to_sync)
    print(f'{all_day_only} {events_description}: {compare_events_lists(set(src_events), set(dst_events))}')
