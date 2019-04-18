from datetime import datetime

from modules.calendar.reminder_queue import ReminderQueue


class TimeManager:

    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.queue = ReminderQueue(self.event_manager.get_all_events())

    def delete_obsolete(self):
        """
        This method removes all events that have already happened; or changes their dates if they are recurring.
        """
        # Get all events. Automatically sorted by date.
        events = self.event_manager.get_all_events()
        for event in events:
            if event["date"] < datetime.now():
                if event["recur"]:
                    self.event_manager.event_recur(event[self.event_manager.model.PRIMARY_KEY])
                else:
                    self.event_manager.delete_event(event[self.event_manager.model.PRIMARY_KEY])
            else:
                break

    def check_reminders(self):
        """
        This method checks whether the reminder queue needs to be rebuilt.
        """
        if self.event_manager.altered:
            self.queue.clear()
            self.queue.build_queue(self.event_manager.get_all_events())

    def send_reminders(self):
        """
        This method will check if any reminders need to be sent.
        :return: A list of reminders that need to be sent.
        """
        list_of_reminders = []
        next_reminder = self.queue.pop_queue()
        while next_reminder:
            list_of_reminders.append(next_reminder)
            next_reminder = self.queue.pop_queue()
        return list_of_reminders

    def clock_pass(self):
        """
        This message will send reminders and handle events that have happened.
        :return: A list of reminders that need to be sent.
        """
        reminders = self.send_reminders()
        self.delete_obsolete()
        self.check_reminders()
        return reminders
