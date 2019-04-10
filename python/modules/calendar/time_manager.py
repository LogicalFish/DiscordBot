from datetime import datetime, timedelta

from modules.calendar.reminder_queue import ReminderQueue


class TimeManager:

    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.queue = ReminderQueue(self.event_manager.get_all_events())

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
                    self.event_recur(event[self.event_manager.model.PRIMARY_KEY])
                else:
                    self.event_manager.delete_event(event[self.event_manager.model.PRIMARY_KEY])
            else:
                break

    def check_reminders(self):
        if self.event_manager.altered:
            self.queue.clear()
            self.queue.build_queue(self.event_manager.get_all_events())

    def send_reminders(self):
        list_of_reminders = []
        next_reminder = self.queue.pop_queue()
        while next_reminder:
            list_of_reminders.append(next_reminder)
            next_reminder = self.queue.pop_queue()
        return list_of_reminders

    def clock_pass(self):
        reminders = self.send_reminders()
        self.delete_obsolete()
        self.check_reminders()
        return reminders
