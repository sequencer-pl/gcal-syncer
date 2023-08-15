# gcal-syncer
#### A script for copying full-day events (in a recent version) from one google calendar to another

### Installation

> make install

### Usage

```commandline
$poetry run syncer --help
Usage: syncer [OPTIONS]

  A script for copying full-day events (in a recent version) from one google
  calendar to another

Options:
  -s, --source_calendar_id TEXT   A calendar identifier from data will be
                                  copied. Example:
                                  abc@group.calendar.google.com  [required]
  -d, --destination_calendar_id TEXT
                                  The identifier of a calendar to which data
                                  will be copied. Example:
                                  abc@group.calendar.google.com  [required]
  -a, --all-day-only              At the moment it allows sync only all day
                                  events. This flag is always true.
  -e, --events_description TEXT   Description for added events
  -n, --number_of_days_to_sync INTEGER
                                  How many days from today do you want to
                                  synchronize
  -t, --token_json TEXT           Token json content. Paste it in apostrophes,
                                  E.g. '{"token": "Lorem..."}...'
  --help                          Show this message and exit.

```
