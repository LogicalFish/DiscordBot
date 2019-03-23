import re
import settings
from dateutil import parser


class EventModel:

    TABLE_NAME = "events"
    PRIMARY_KEY = "event_id"

    author_key = "author"

    required_fields = {"name": "VARCHAR({})".format(settings.MAX_EVENT_NAME),
                       "date": "TIMESTAMP",
                       author_key: "VARCHAR(255)"
                       }

    optional_fields = {"description": "VARCHAR({})".format(settings.MAX_EVENT_DESCRIPTION),
                       "channel": "VARCHAR(255)",
                       "tag": "VARCHAR(255)",
                       "reminder": "VARCHAR(255)",
                       "recur": "INTEGER"
                       }

    def validate_required_fields(self, fields):
        for key in self.required_fields.keys():
            if key not in fields.keys():
                raise ValueError("Required field '*{}*' missing.".format(key))

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
                max_length = int(re.findall("\\((\\d+)\\)", model[key])[0])
                if len(input_fields[key]) > max_length:
                    raise ValueError("Field '{}' is too long.".format(key))
            elif model[key] == "TIMESTAMP":
                try:
                    input_fields[key] = parser.parse(input_fields[key], dayfirst=True)
                except ValueError:
                    raise ValueError("'{}' is geen valide tijd/datum combinatie.".format(input_fields[key]))
            elif model[key] == "INTEGER":
                try:
                    input_fields[key] = int(input_fields[key])
                except ValueError:
                    raise ValueError("'{}' is geen valide getal.".format(input_fields[key]))
            if key == "reminder":
                if not re.match("^(\\d+,)+\\d+$", input_fields[key]):
                    raise ValueError("'{}' is geen valide getal voor reminders.".format(input_fields[key]))
            if key == "channel":
                input_fields[key].replace('#', '')

    def create_table_sql(self):
        sql = "{} SERIAL PRIMARY KEY".format(self.PRIMARY_KEY)
        for key in self.required_fields.keys():
            sql += ", {} {} NOT NULL".format(key, self.required_fields[key])
        for key in self.optional_fields.keys():
            sql += ", {} {}".format(key, self.optional_fields[key])
        sql = "CREATE TABLE {} ( {} );".format(self.TABLE_NAME, sql)
        return sql
