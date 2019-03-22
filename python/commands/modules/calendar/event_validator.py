import re
from dateutil import parser

DEFAULT_TIME = "12:00"


def string_to_dictionary(string):
    parsed = re.findall("(\\w*)\\s*=\\s*\"(.*?)\"", string)
    result = {}
    for r in parsed:
        result[r[0].lower()] = r[1]
    return result


def validate_input(user_dict):
    # Check if required fields are there.

    return True


def clean_input(user_input, db_man):
    input_dict = string_to_dictionary(user_input)
    input_dict["date"] = clean_date(input_dict["date"], input_dict.get("time", DEFAULT_TIME))
    input_dict = remove_non_columns(input_dict, db_man)

    return input_dict


def clean_date(date, time):
    datetime = "{}, {}".format(time, date)
    try:
        return parser.parse(datetime, dayfirst=True)
    except ValueError:
        raise ValueError("'{}' is geen valide tijd/datum combinatie.".format(datetime))


def remove_non_columns(user_dict, db_man):
    key_list = list(user_dict.keys())
    columns = db_man.get_columns('events')
    for key in key_list:
        if key not in columns:
            user_dict.pop(key)
    return user_dict
