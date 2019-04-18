from datetime import timedelta
from modules.calendar import event_reader
import settings

"""
Methods to deal with 'shadow events': Events which would happen when recurring events would happen.
For example, event A happens this sunday, and happens every week. The first shadow event would take place
the sunday after next.
"""


def get_shadow_events(event, quantity):
    """
    Method to get a list of shadow events.
    :param event: The event you want to obtain shadow events of.
    :param quantity: The amount of shadow events you want, up to a maximum set in settings.
    :return: A list of shadow events
    """
    shadow_events = []
    if "recur" in event and event["recur"] is not None:
        new_event = event.copy()
        shadow_time = timedelta(days=event["recur"])
        for i in range(min(quantity, settings.MAX_SHADOW)):
            new_event["date"] = new_event["date"] + shadow_time
            new_event["event_id"] = "{}-{}".format(event["event_id"], (i+1))
            shadow_events.append(new_event)
            new_event = new_event.copy()

    return shadow_events


def get_list_shadow(events, quantity):
    """
    Method to get a list of shadow events from multiple events, each sorted by date.
    :param events: A complete list of events.
    :param quantity: The amount of shadow events you want, up to a maximum set in settings.
    :return: A list of both events and shadow events, sorted by date.
    """
    list_with_shadow = []
    for event in events:
        event_tuple = (event["date"], event_reader.describe_short(event))
        list_with_shadow.append(event_tuple)
        shadow_events = get_shadow_events(event, quantity)
        for shadow_event in shadow_events:
            event_tuple = (shadow_event["date"], event_reader.describe_shadow(shadow_event))
            list_with_shadow.append(event_tuple)
    list_with_shadow = sorted(list_with_shadow)
    return list_with_shadow
