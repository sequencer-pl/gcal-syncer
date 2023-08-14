from syncer.dataclasses.calendar import Event


# def compare_events_lists(first: set[Event], second: set[Event]) -> tuple[set[Event], set[Event]]:
#     return (
#         set(first).difference(set(second)),
#         set(second).difference(set(first))
#     )

def compare_events_lists(first: list[Event], second: list[Event]) -> tuple[list[Event], list[Event]]:
    return (
        [e for e in first if e not in second],
        [e for e in second if e not in first]
    )
