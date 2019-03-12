from datetime import datetime, timedelta

from dateutil import parser
import settings as s


class Event:
    DEFAULT_TIME="12:00"
    DATE_FORMAT="%a %d %B, %Y"
    TIME_FORMAT="%H:%M"

    def __init__(self, owner, var_dict):
        if "name" not in var_dict or "date" not in var_dict:
            raise EventError("Er is geen naam of datum gevonden. Dit zijn nodige parameters.")
        else:
            self.owner = owner
            #DEFAULTS
            self.name = None
            self.planning = None
            self.description = ""
            self.tag = ""
            self.reminders = []
            self.recurring = False
            self.channel = ""
            #Init values
            self.add_vars(var_dict)

    def __str__(self):
        result = "**Name:** {}.\n" \
                 "**Description:** {}\n" \
                 "**Date:** {}\n" \
                 "**Time:** {}" \
            .format(self.name,
                    self.description,
                    self.planning.strftime(self.DATE_FORMAT),
                    self.planning.strftime(self.TIME_FORMAT))
        return result

    def display_date(self):
        return self.planning.strftime("{}, {}".format(self.DATE_FORMAT, self.TIME_FORMAT))

    def add_vars(self, var_dict):
        if "name" in var_dict:
            self.name = var_dict["name"][:s.MAX_EVENT_NAME]
        if "description" in var_dict:
            self.description = var_dict["description"][:s.MAX_EVENT_DESCRIPTION]
        if "tag" in var_dict:
            self.tag = var_dict["tag"]
        if "date" in var_dict or "time" in var_dict:
            if self.planning:
                self.add_date_time(
                    var_dict.get("date", self.planning.strftime(self.DATE_FORMAT)),
                    var_dict.get("time", self.planning.strftime(self.TIME_FORMAT))
                )
            else:
                self.add_date_time(var_dict["date"], var_dict.get("time", self.DEFAULT_TIME))
        if "reminder" in var_dict:
            self.add_reminders(var_dict["reminder"])
        if "channel" in var_dict:
            self.channel = var_dict["channel"].replace('#','')
        if "recur" in var_dict:
            self.add_recurring(var_dict["recur"])

    def add_date_time(self, date, time):
        time_date = "{}, {}".format(time, date)
        try:
            self.planning = parser.parse(time_date, dayfirst=True)
        except ValueError:
            raise EventError("'{}' is geen valide tijd/datum combinatie.".format(time_date))
        if self.planning < datetime.now():
            raise EventError("'{}' is in het verleden.".format(self.planning))

    def add_reminders(self, user_input):
        self.reminders = []
        if len(user_input):
            remind_array = user_input.split(',')
            for reminder in remind_array:
                try:
                    i = float(reminder)
                    remindertime = self.planning - timedelta(hours=i)
                    if i > 0 and remindertime > datetime.now():
                        self.reminders.append(remindertime)
                except ValueError:
                    raise EventError("'{}' is geen valide getal voor reminders".format(user_input))

    def add_recurring(self, user_input):
        try:
            value = int(user_input)
        except:
            raise EventError("'{}' is geen valide getal.".format(user_input))
        if value > 365:
            raise EventError("'{}' is geen valide aantal dagen.".format(value))
        if value <= 0:
            self.recurring = False
        else:
            self.recurring = timedelta(days=value)


class EventError(Exception):
    """
    Special Error Class, to be thrown when an event is not initialized correctly.
    """

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return str(self.message)
