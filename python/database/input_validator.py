from datetime import datetime
from dateutil import parser
import re


def validate_varchar(char_input, varchar_value):
    max_length = int(re.findall("\\((\\d+)\\)", varchar_value)[0])
    if len(char_input) > max_length:
        raise ValueError("Field '{}' is too long.".format())


def clean_integer(number_input):
    try:
        return int(number_input)
    except ValueError:
        raise ValueError("'{}' is geen valide getal.".format(number_input))


def clean_future_date(date_input):
    try:
        date_output = parser.parse(date_input, dayfirst=True)
    except ValueError:
        raise ValueError("'{}' is geen valide tijd/datum combinatie.".format(date_input))
    if date_output < datetime.now():
        raise ValueError("'{}' is in het verleden.".format(date_input))
    return date_output


