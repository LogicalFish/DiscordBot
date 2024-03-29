from datetime import datetime


class ReminderQueue:
    """
    Class for keeping track of when to send out event reminders.
    """

    def __init__(self, events):
        self.queue = []
        self.build_queue(events)

    def __str__(self):
        string = ""
        for event in self.queue:
            string += "{} : {}\n".format(event[0], event[1])
        return string

    def build_queue(self, events):
        """
        Method to form the queue of reminders.
        :param events: A list of events of which to generate reminders.
        """
        for event in events:
            for time, embed in event.get_reminders():
                if time > datetime.now():
                    self.queue.append((time, embed, event.channel, event.tag))
        self.queue.sort(key=lambda tup: tup[0])

    def clear(self):
        """
        Method to clear the queue.
        """
        self.queue.clear()

    def pop_queue(self):
        """
        Method to request a reminder.
        :return: The first reminder in the queue, if it is ready. False if no reminder is ready.
        """
        if self.queue and self.queue[0][0] < datetime.now():
            return self.queue.pop(0)
        else:
            return False
