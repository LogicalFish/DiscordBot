import re
import operator

import config
from commands.command_error import CommandError
from commands.command_superclass import Command

from modules.characterlist import npc_tracker, npc_trackers


class ListAllCommand(Command):

    def __init__(self):
        call = ["list", "listall", "npcs"]
        parameters = "Search parameters (optional)"
        description = "This command will list all characters that match the search parameters.\n" \
                      "A search parameter has the shape x=\"Y\"." \
                      "A list of all possible parameters:\n" \
                      "\t*name*\n" \
                      "\t*names.title*\n\t*names.firstname*\n\t*names.middle*\n\t*names.nickname*\n\t*names.surname*\n\t*names.moniker*\n" \
                      "\t*gender*\n\t*race*\n\t*subrace*\n\t*class*\n\t*location*\n\t*birthyear*\n" \
                      "\t*organization.name*\n\t*organization.rank*\n\t*organization.status*\n" \
                      "\t*description*\n"
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        parsed = re.findall("([\\w\\.]*)\\s*=\\s*[\"'](.*?)[\"']", param)
        search_tuples = []
        for r in parsed:
            search_tuples.append((r[0], r[1]))
        npc_list = []
        for tracker in npc_trackers:
            npc_list += tracker.get_list_of_npcs(search_tuples)
        npc_list.sort(key=operator.attrgetter("sort_key", "secondary_sort_key"))

        preamble = "Er zijn {} karakters gevonden:\n".format(len(npc_list))
        response = format_npc_name_list(npc_list, preamble)
        return {"response": response}


class WhoIsCommand(Command):

    def __init__(self):
        call = ["whois", "findnpc"]
        parameters = "The name of the character you wish to find."
        description = "This command will find a character matching the name, or a list of characters if multiple match."
        super().__init__(call, parameters, description)
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
            action = {"response": "Er is geen karakter met die naam gevonden."}
        elif len(npc_list) == 1:
            npc = npc_list[0]
            action = {"embed": npc.get_npc_embed()}
        elif len(npc_list) > 1:
            self.saved_list = npc_list
            preamble = "Er zijn {} karakters gevonden. Specificeer welke je zoekt voor meer informatie:\n".format(len(npc_list))
            multi_response = format_npc_name_list(npc_list, preamble)
            action = {"response": multi_response}
        else:
            action = {"response": "ERROR"}
        return action


class GetYearCommand(Command):

    def __init__(self):
        call = ["year", "getyear", "whatyear"]
        parameters = "None."
        description = "A Command to request the setting's current year."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        response = ""
        for tracker in npc_trackers:
            if len(param) == 0 or tracker.name in param:
                response += "The current year of {} is {}.\n".format(tracker.name, tracker.current_year)
        if len(response) == 0:
            raise CommandError("invalid_parameter", param)
        return {"response": response}


class AddYearCommand(Command):

    def __init__(self):
        call = ["addyear", "yearup"]
        parameters = "A number declaring how many years to add. (optional)"
        description = "A command that can be used by the DM to alter the current year."
        super().__init__(call, parameters, description)

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
                response = "Time has passed since year {} of {}. It is now the year {}.".format(tracker.name,
                                                                                                old_year,
                                                                                                tracker.current_year)
                return {"response": response}
        raise CommandError("command_not_allowed", None)


def format_npc_name_list(npc_list, preamble):
    npc_name_list = preamble
    name_list = ["**{}.** {}".format(count + 1, npc.get_name()) for count, npc in enumerate(npc_list)]
    max_reached = "- *etc. (character limit reached)*"
    for name in name_list:
        if len(npc_name_list) + len(name) + len(max_reached) < config.CHARACTER_MAX:
            npc_name_list += "{}\n".format(name)
        else:
            npc_name_list += max_reached
            break
    return npc_name_list
