import re
import operator

import config
from commands.command_error import CommandError
from commands.command_superclass import Command

from modules.characterlist import npc_trackers


class ListAllCommand(Command):

    def __init__(self):
        super().__init__('list_npcs')

    def execute(self, param, message, system):
        parsed = re.findall("([\\w.]*)\\s*=\\s*[\"'](.*?)[\"']", param)
        search_tuples = []
        for r in parsed:
            search_tuples.append((r[0], r[1]))
        npc_list = []
        for tracker in npc_trackers:
            npc_list += tracker.get_list_of_npcs(search_tuples)
        npc_list.sort(key=operator.attrgetter("sort_key", "secondary_sort_key"))

        preamble = config.localization[self.name]['prefix'].format(len(npc_list))
        response = format_npc_name_list(npc_list, preamble)
        return {"response": response}


class WhoIsCommand(Command):

    def __init__(self):
        super().__init__('who_is_npc')
        self.saved_list = []

    def execute(self, param, message, system):
        if param.isdigit() and len(self.saved_list) > 0:
            list_number = int(param) - 1
            if list_number < len(self.saved_list):
                npc = self.saved_list[list_number]
                action = {"embed": npc.get_npc_embed()}
                return action
        npc_list = []
        score = 0
        for tracker in npc_trackers:
            new_list, new_score = tracker.get_npcs_by_name_only(param)
            if new_score == score:
                npc_list += new_list
            if new_score > score:
                npc_list = new_list
                score = new_score
        npc_list.sort(key=operator.attrgetter("sort_key", "secondary_sort_key"))

        if len(npc_list) == 0:
            action = {"response": config.localization[self.name]['no_npcs']}
        elif len(npc_list) == 1:
            npc = npc_list[0]
            action = {"embed": npc.get_npc_embed()}
        elif len(npc_list) > 1:
            self.saved_list = npc_list
            preamble = config.localization[self.name]['multiple_npcs'].format(len(npc_list))
            multi_response = format_npc_name_list(npc_list, preamble)
            action = {"response": multi_response}
        else:
            action = {"response": "ERROR"}
        return action


class GetYearCommand(Command):

    def __init__(self):
        super().__init__('get_year')

    def execute(self, param, message, system):
        response = ""
        for tracker in npc_trackers:
            if len(param) == 0 or tracker.name in param:
                response += config.localization[self.name]['response'].format(tracker.name, tracker.current_year)
        if len(response) == 0:
            raise CommandError("invalid_parameter", param)
        return {"response": response}


class AddYearCommand(Command):

    def __init__(self):
        super().__init__('add_year')

    def execute(self, param, message, system):
        for tracker in npc_trackers:
            if tracker.owner == message.author.id:
                old_year = tracker.current_year
                if param:
                    try:
                        years = int(param)
                        tracker.year_up(years)
                    except ValueError:
                        tracker.year_up()
                else:
                    tracker.year_up()
                response = config.localization[self.name]['response'].format(tracker.name,
                                                                             old_year,
                                                                             tracker.current_year)
                return {"response": response}
        raise CommandError("command_not_allowed", None)


def format_npc_name_list(npc_list, preamble):
    npc_name_list = preamble
    name_list = ["**{}.** {}".format(count + 1, npc.get_name()) for count, npc in enumerate(npc_list)]
    max_reached = config.localization['npc_character_limit']
    for name in name_list:
        if len(npc_name_list) + len(name) + len(max_reached) < config.configuration['max_msg_length']:
            npc_name_list += "{}\n".format(name)
        else:
            npc_name_list += max_reached
            break
    return npc_name_list
