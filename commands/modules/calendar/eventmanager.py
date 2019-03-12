import re
from datetime import timedelta

import settings as s
from commands.modules.calendar.event import Event, EventError


class EventManager:

    def __init__(self):
        self.events = {}
        self.id_count = 1

    def parse_string(self, text, channel):
        parsed = re.findall("(\\w*)\s*=\s*\"(.*?)\"", text)
        result = {}
        for r in parsed:
            result[r[0].lower()] = r[1]
        if "channel" not in result:
            result["channel"] = channel
        return result

    def create_event(self, user_input, user, default_channel=""):
        var_dict = self.parse_string(user_input, default_channel)
        times = 1
        add = 0
        if "multiply" in var_dict:
            times_match = re.search("\*(\d+)", var_dict["multiply"])
            add_match = re.search("\+(\d+)", var_dict["multiply"])
            if times_match:
                times = min(int(times_match.group(1)), s.MAX_EVENTS)
            if add_match:
                add = min(int(add_match.group(1)), s.MAX_INTERVAL)

        for t in range(times):

            try:
                new_event = Event(user, var_dict)
                new_event.planning += timedelta(days=add*t)
            except EventError as ee:
                return "[ERROR]: {}".format(ee)

            self.events[self.id_count] = new_event
            self.id_count += 1
        if times == 1:
            output = "Er is 1 nieuwe event toegevoegd:\n{}".format(new_event)
        else:
            output = "Er zijn {} nieuwe events toegevoegd:\n{}".format(times, self.list_events())
        return output

    def edit_event(self, user_input, user):
        var_dict = self.parse_string(user_input)
        if "id" in var_dict:
            id_str = var_dict["id"]
        else:
            id_str = user_input.split(' ', 1)[0]
        try:
            identifier = int(id_str)
        except ValueError:
            return "[ERROR]: Id '{}' is geen valide ID".format(id_str)

        if identifier in self.events:
            edited_event = self.events[identifier]
            if edited_event.owner != user:
                return "[ERROR]: Jij bent niet de eigenaar van dit event."
            try:
                edited_event.add_vars(var_dict)
            except EventError as ee:
                return "[ERROR]: {}".format(ee)
            return edited_event
        else:
            return "[ERROR]: Geen event met ID '{}' gevonden".format(identifier)

    def list_events(self):
        result = ""
        event_list = list(self.events.items())
        if len(event_list):
            event_list.sort(key=lambda event_list: event_list[1].planning)
            i=0
            while i < len(event_list):
                entry = event_list[i]
                result += "*{}* - **Event {}:** {}.\n".format(entry[1].display_date(), entry[0], entry[1].name)
                # if entry[1].recurring:
                i+=1
        else:
            result = "Ik heb geen evenementen gevonden."
        return result

    def show_event(self, identifier):
        try:
            i = int(identifier)
            if i in self.events:
                return self.events[i]
            else:
                return "[ERROR]: Geen event met ID '{}' gevonden".format(i)
        except ValueError:
            return "[ERROR]: ID '{}' is geen valide ID".format(identifier)

    def delete_event(self, identifier, user):
        try:
            i = int(identifier)
            if i in self.events:
                if self.events[i].owner == user:
                    self.events.pop(i)
                    return "Deleted event {}.".format(i)
                else:
                    return "[ERROR]: Jij bent niet de eigenaar van dit evenement."
            else:
                return "[ERROR]: Geen event met ID '{}' gevonden".format(i)
        except ValueError:
            return "[ERROR]: ID '{}' is geen valide ID".format(identifier)

