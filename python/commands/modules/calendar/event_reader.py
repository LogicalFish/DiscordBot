import re

DATE_FORMAT = "%a %d %B, %Y"
TIME_FORMAT = "%H:%M"


def display_date(datetime):
    return datetime.strftime("{}, {}".format(DATE_FORMAT, TIME_FORMAT))


def describe_short(event):
    description = "*{}* - **Event {}:** {}.\n".format(display_date(event["date"]), event["event_id"], event["name"])
    return description


def describe_long(event):
    description = "**Name:** {}.\n" \
                  "**Description:** {}\n" \
                  "**Date:** {}\n" \
                  "**Time:** {}".format(event["name"],
                                        event["description"],
                                        event["date"].strftime(DATE_FORMAT),
                                        event["date"].strftime(TIME_FORMAT))
    return description


def create_event_dict(string):
    parsed = re.findall("(\\w*)\\s*=\\s*\"(.*?)\"", string)
    output_dict = {}
    for r in parsed:
        output_dict[r[0].lower()] = r[1]

    return output_dict