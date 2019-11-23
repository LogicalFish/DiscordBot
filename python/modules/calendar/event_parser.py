import re
from datetime import datetime
from dateutil import parser

from modules.calendar import calendar_config


def parse_string(string_input, max_length, key):
    if len(string_input) > max_length:
        raise EventError("string_too_long", key)
    return string_input


def parse_date(date_input):
    try:
        date_output = parser.parse(date_input, dayfirst=True)
    except ValueError:
        raise EventError("invalid_date", date_input)
    if date_output < datetime.now():
        raise EventError("invalid_future_date", date_input)
    return date_output


def parse_integer(number_input):
    try:
        return int(number_input)
    except ValueError:
        raise EventError("number_not_valid", number_input)


def parse_int_array(array_input):
    numbers = re.findall("(\\d+)", array_input)
    result = []
    for number in numbers:
        result.append(int(number))
    if len(result) > 0:
        return result
    else:
        raise EventError("invalid_reminder", array_input)


def parse_event_string(string):
    parsed = re.findall("(\\w*)\\s*=\\s*\"(.*?)\"", string)
    output_dict = {}
    for r in parsed:
        category = r[0].lower()
        if r[0].lower() in calendar_config.SYNONYMS:
            category = calendar_config.SYNONYMS[r[0].lower()]
        if category in output_dict:
            output_dict[category] += ", " + r[1]
        else:
            output_dict[category] = r[1]
    return output_dict


class EventError(Exception):
    """
    Special Error Class, to be thrown when an event is not initialized correctly.
    """

    def __init__(self, message, parameters):
        super().__init__(message)
        self.message = message
        self.parameters = parameters

    def __str__(self):
        return str(self.message)
