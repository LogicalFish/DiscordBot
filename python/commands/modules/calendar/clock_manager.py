import math
from datetime import datetime, timedelta


class TimeManager:

    def __init__(self, event_manager):
        self.event_manager = event_manager

    def event_recur(self, id_no):
        event = self.event_manager.get_event(id_no)
        if event["recur"]:
            next_time = timedelta(days=event["recur"])
            new_date = event["date"] + next_time
            self.event_manager.update_event(id_no, {"date": new_date})

    def delete_obsolete(self):
        #Get all events. Automatically sorted by date.
        events = self.event_manager.get_all_events()
        for event in events:
            if event["date"] < datetime.now():
                if event["recur"]:
                    self.event_recur(event["event_id"])
                else:
                    self.event_manager.delete_event(events[0][self.event_manager.primary_key])
            else:
                break

    def get_reminder(self, id_no):
        event = self.event_manager.get_event(id_no)
        #Pass Reminder Code



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
