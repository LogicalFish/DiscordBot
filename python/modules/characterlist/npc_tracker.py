import config
from modules.characterlist import query_tree
from modules.characterlist.character_info import CharacterInfo
import operator


class NPCTracker:

    def __init__(self, owner, year):
        self.owner = owner
        self.current_year = year
        self.forbidden_knowledge = ["deathyear"]
        # self.allowed_stats = ["gender", "race", "subrace", "class", "location", "birthyear", "organization.name", "organization.rank", "organization.status"]

    def year_up(self, number=1):
        self.current_year += number

    def get_list_of_npcs(self, search_tuples):
        search_tree = query_tree.root
        for search_tuple in search_tuples:
            if search_tuple[0].lower() == "name":
                search_tree = query_tree.find_npcs_by_name(search_tuple[1], search_tree)
            elif search_tuple[0].lower() == "alive":
                not_alive = False
                if search_tuple[1].lower() == "false":
                    not_alive = True
                search_tree = query_tree.filter_living_npcs(self.current_year, search_list=search_tree, death=not_alive)
            elif search_tuple[0].lower() in self.forbidden_knowledge:
                pass
            else:
                search_tree = query_tree.find_npcs_by_category(search_tuple[0], search_tuple[1], search_tree)
        final_list = []
        for found_item in search_tree:
            npc = CharacterInfo(query_tree.item_to_dictionary(found_item), self.current_year)
            final_list.append(npc)
        final_list.sort(key=operator.attrgetter("sort_key", "secondary_sort_key"))
        return final_list

    def get_npc_name_list(self, npc_list, preamble):
        npc_name_list = preamble
        name_list = ["**{}.** {}".format(count+1, npc.get_name()) for count, npc in enumerate(npc_list)]
        max_reached = "- *etc. (character limit reached)*"
        for name in name_list:
            if len(npc_name_list) + len(name) + len(max_reached) < config.CHARACTER_MAX:
                npc_name_list += "{}\n".format(name)
            else:
                npc_name_list += max_reached
                break
        return npc_name_list

    # def get_stats(self, category):
    #     if category in self.allowed_stats:
    #         statistics = query_tree.get_stats(category)
    #         result = ""
    #         for data_point in sorted(statistics, key=statistics.get, reverse=True):
    #             result += "**{}**: {}\n".format(data_point, statistics[data_point])
    #         return result
    #     else:
    #         return "Sorry, could not collect statistics in the *{}* category.".format(category)
