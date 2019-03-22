import math
from datetime import datetime


class TimeManager:

    def __init__(self, event_manager):
        self.event_manager = event_manager

    def delete_obsolete(self):
        key_list = list(self.event_manager.events.keys())
        for key in key_list:
            event = self.event_manager.events[key]
            if event.planning < datetime.now():
                if event.recurring:
                    event.planning += event.recurring
                else:
                    self.event_manager.events.pop(key)

    def reminders(self):
        result = []
        for key in self.event_manager.events:
            event = self.event_manager.events[key]
            for i, reminder in enumerate(event.reminders):
                if reminder < datetime.now():
                    delta = event.planning - datetime.now()
                    message = "Event {}: **{}** happens in {}!".format(key, event.name, get_time_string(delta))
                    result.append((message, event.channel, event.tag))
                    if event.recurring:
                        event.reminders[i] = reminder + event.recurring
                    else:
                        event.reminders.remove(reminder)
        return result


def get_time_string(delta):
    if delta.days > 0:
        accurate_time = round(delta.total_seconds / (60 * 60 * 24))
        result = "{} day".format(accurate_time)
        if accurate_time > 1:
            result += "s"
        return result
    minutes = math.ceil(delta.total_seconds()/60)
    if minutes > 120:
        return "{0:g} hours".format(round(minutes/60, 1))
    return "{} minutes".format(minutes)
