from datetime import timedelta
from commands.modules.calendar import event_reader

MAX_SHADOW = 9


def get_shadow_events(event, quantity):
    shadow_events = []
    if "recur" in event:
        new_event = event.copy()
        shadow_time = timedelta(days=event["recur"])
        for i in range(min(quantity, MAX_SHADOW)):
            new_event["date"] = new_event["date"] + shadow_time
            new_event["event_id"] = "{}-{}".format(event["event_id"], (i+1))
            shadow_events.append(new_event)
            new_event = new_event.copy()

    return shadow_events


def get_list_shadow(events, quantity):
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


# from dateutil import parser
#
# test_event = {"event_id": 1, "name": "noym", "date": parser.parse("25 March, 12:00", dayfirst=True), "recur": 7}
# print("{}: {}".format(test_event["date"], test_event))
# shadow_events = get_shadow_events(test_event, 3)
# for event in shadow_events:
#     print("{}: {}".format(event["date"],event))
