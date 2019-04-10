import re
import settings
from datetime import datetime
from dateutil import parser

# from database import input_validator as validator


class EventModel:

    TABLE_NAME = "events"
    PRIMARY_KEY = "event_id"

    key_date = "date"
    key_author = "author"

    required_fields = {"name": "VARCHAR({})".format(settings.MAX_EVENT_NAME),
                       key_date: "TIMESTAMP",
                       key_author: "VARCHAR(255)"
                       }

    optional_fields = {"description": "VARCHAR({})".format(settings.MAX_EVENT_DESCRIPTION),
                       "channel": "VARCHAR(255)",
                       "tag": "VARCHAR(255)",
                       "reminder": "INTEGER[]",
                       "recur": "INTEGER"
                       }

    def validate_required_fields(self, fields):
        for key in self.required_fields.keys():
            if key not in fields.keys():
                raise EventError("required_field_missing", key)

    def prune_fields(self, fields):
        key_list = list(fields.keys())
        for key in key_list:
            if key not in self.required_fields and key not in self.optional_fields:
                fields.pop(key)
            elif key == "creator":
                fields.pop(key)

    def clean_data(self, input_fields):
        self.prune_fields(input_fields)
        model = {**self.required_fields, **self.optional_fields}
        for key in input_fields.keys():
            if model[key].startswith("VARCHAR"):
                self.validate_varchar(input_fields[key], model[key], key)
            elif model[key] == "TIMESTAMP":
                input_fields[key] = self.clean_future_date(input_fields[key])
            elif model[key] == "INTEGER":
                input_fields[key] = self.clean_integer(input_fields[key])
            elif model[key] == "INTEGER[]":
                if re.match("^(\\d+,\\s*)+\\d+$", input_fields[key]):
                    input_fields[key] = "{{ {} }}".format(input_fields[key])
                else:
                    raise EventError("invalid_reminder", input_fields[key])

    def create_table_sql(self):
        sql = "{} SERIAL PRIMARY KEY".format(self.PRIMARY_KEY)
        for key in self.required_fields.keys():
            sql += ", {} {} NOT NULL".format(key, self.required_fields[key])
        for key in self.optional_fields.keys():
            sql += ", {} {}".format(key, self.optional_fields[key])
        sql = "{} ( {} );".format(self.TABLE_NAME, sql)
        return sql

    def validate_varchar(self, char_input, varchar_value, key):
        max_length = int(re.findall("\\((\\d+)\\)", varchar_value)[0])
        if len(char_input) > max_length:
            raise EventError("string_too_long", key)

    def clean_integer(self, number_input):
        try:
            return int(number_input)
        except ValueError:
            raise ValueError("number_not_valid", number_input)

    def clean_future_date(self, date_input):
        try:
            date_output = parser.parse(date_input, dayfirst=True)
        except ValueError:
            raise ValueError("invalid_date", date_input)
        if date_output < datetime.now():
            raise ValueError("invalid_future_date", date_input)
        return date_output


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
