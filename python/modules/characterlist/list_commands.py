import re

from commands.command_error import CommandError
from commands.command_superclass import Command

from modules.characterlist import npc_tracker


class ListAllCommand(Command):

    def __init__(self):
        call = ["list", "listall", "npcs"]
        parameters = "Search parameters (optional)"
        description = "This command will list all NPCs that match the search parameters.\n" \
                      "A search parameter has the shape x='y'. Example: race='human', or organization.name='winged men'"
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        parsed = re.findall("([\\w\\.]*)\\s*=\\s*\"(.*?)\"", param)
        search_tuples = []
        for r in parsed:
            search_tuples.append((r[0], r[1]))

        npc_list = npc_tracker.get_list_of_npcs(search_tuples)

        preamble = "Er zijn {} karakters gevonden:\n".format(len(npc_list))
        message = npc_tracker.get_npc_name_list(npc_list, preamble)
        return {"response": message}


class WhoIsCommand(Command):

    def __init__(self):
        call = ["whois", "findnpc"]
        parameters = "The name of the character you wish to find."
        description = "This command will find a character matching the name, or a list of characters if multiple match."
        super().__init__(call, parameters, description)
        self.saved_list = []

    def execute(self, param, message, system):
        print(param)
        print(param.isdigit())
        print(len(self.saved_list))
        if param.isdigit() and len(self.saved_list) > 0:
            list_number = int(param) - 1
            print(list_number)
            if list_number < len(self.saved_list):
                npc = self.saved_list[list_number]
                action = {"embed": npc.get_npc_embed()}
                return action
        npc_list = npc_tracker.get_list_of_npcs([("name", param)])
        if len(npc_list) == 0:
            action = {"response": "Er is geen karakter met die naam gevonden."}
        elif len(npc_list) == 1:
            npc = npc_list[0]
            action = {"embed": npc.get_npc_embed()}
        elif len(npc_list) > 1:
            self.saved_list = npc_list
            preamble = "Er zijn {} karakters gevonden. Specificeer welke je zoekt voor meer informatie:\n".format(len(npc_list))
            multi_response = npc_tracker.get_npc_name_list(npc_list, preamble)
            action = {"response": multi_response}
        return action


class GetYearCommand(Command):

    def __init__(self):
        call = ["year", "getyear", "whatyear"]
        parameters = "None."
        description = "A Command to request the setting's current year."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        message = "The current year of the Chaos is {}.".format(npc_tracker.current_year)

        return {"response": message}


class AddYearCommand(Command):

    def __init__(self):
        call = ["addyear", "yearup"]
        parameters = "A number declaring how many years to add. (optional)"
        description = "A command that can be used by the DM to alter the current year."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        if npc_tracker.owner == message.author.id:
            old_year = npc_tracker.current_year
            if param:
                try:
                    years = int(param)
                    npc_tracker.year_up(years)
                except ValueError:
                    npc_tracker.year_up()
            else:
                npc_tracker.year_up()
            message = "Time has passed since year {} of Chaos. It is now the year {}.".format(old_year,
                                                                                         npc_tracker.current_year)
            return {"response": message}
        else:
            raise CommandError("command_not_allowed", None)

