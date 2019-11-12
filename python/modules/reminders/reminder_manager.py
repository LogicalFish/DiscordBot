import re
from datetime import datetime, timedelta


class ReminderManager:

    def __init__(self):
        self.reminders = []

    def add_reminder(self, delta, message_string, target):
        self.reminders.append((datetime.now() + delta, message_string, target))
        self.reminders.sort(key=lambda tup: tup[0])

    def pop_reminder(self):
        """
        Method to request a reminder.
        :return: The first reminder in the queue, if it is ready. False if no reminder is ready.
        """
        if self.reminders and self.reminders[0][0] < datetime.now():
            return self.reminders.pop(0)
        else:
            return False

    def get_all_reminders(self):
        """
        This method will check if any reminders need to be sent.
        :return: A list of reminders that need to be sent.
        """
        list_of_reminders = []
        next_reminder = self.pop_reminder()
        while next_reminder:
            list_of_reminders.append(next_reminder)
            next_reminder = self.pop_reminder()
        return list_of_reminders
