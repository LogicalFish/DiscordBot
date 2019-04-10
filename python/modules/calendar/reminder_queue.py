from datetime import datetime, timedelta
from modules.calendar import event_reader


class ReminderQueue:

    def __init__(self, events):
        self.queue = []
        self.build_queue(events)

    def __str__(self):
        string = ""
        for event in self.queue:
            string += "{} : {}\n".format(event[0], event[1])
        return string

    def build_queue(self, events):
        for event in events:
            if event["reminder"]:
                reminder_list = sorted(event["reminder"], reverse=True)
                for reminder in reminder_list:
                    message = event_reader.describe_reminder(event, reminder)
                    reminder_time = event["date"] - timedelta(hours=reminder)
                    if reminder_time > datetime.now():
                        self.queue.append((reminder_time, message, event["channel"], event["tag"]))
        self.queue.sort()

    def clear(self):
        self.queue.clear()

    def pop_queue(self):
        if self.queue and self.queue[0][0] < datetime.now():
            return self.queue.pop(0)
        else:
            return False
