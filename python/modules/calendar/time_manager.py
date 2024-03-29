import operator
from datetime import datetime
import logging
from modules.calendar.reminder_queue import ReminderQueue

logger = logging.getLogger(__name__)


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
        events.sort(key=operator.attrgetter('date'))
        for event in events:
            if event.date < datetime.now():
                if event.recur:
                    logger.info("Event {} has expired. Event wil be moved to new date and time.".format(event.event_id))
                    self.event_manager.recur_event(event.event_id)
                else:
                    logger.info("Event {} has expired. Removing the event from the calendar.".format(event.event_id))
                    self.event_manager.delete_event(event.event_id)
            else:
                break

    def check_reminders(self):
        """
        This method checks whether the reminder queue needs to be rebuilt.
        """
        if self.event_manager.altered:
            logger.debug("Events have been altered. Rebuilding reminder queue.")
            self.event_manager.altered = False
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
