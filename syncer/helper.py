from syncer.dataclasses.calendar import Event


def compare_events_lists(first: set[Event], second: set[Event]) -> tuple[set[Event], set[Event]]:
    return (
        set(first).difference(set(second)),
        set(second).difference(set(first))
    )
