import config
from modules.characterlist import query_tree
from modules.characterlist.character_info import CharacterInfo
import operator


class NPCTracker:

    def __init__(self, owner, year):
        self.owner = owner
        self.current_year = year

    def year_up(self, number=1):
        self.current_year += number

    def get_list_of_npcs(self, search_tuples):
        search_tree = query_tree.root
        for search_tuple in search_tuples:
            if search_tuple[0].lower() == "any":
                search_tree = query_tree.find_npcs_by_any(search_tuple[1], search_tree)
            elif search_tuple[0].lower() == "name":
                search_tree = query_tree.find_npcs_by_name(search_tuple[1], search_tree)
            elif search_tuple[0].lower() == "alive":
                not_alive = (search_tuple[1].lower() == "false")
                search_tree = query_tree.filter_living_npcs(self.current_year, search_list=search_tree, death=not_alive)
            elif search_tuple[0].lower() == "deathyear":
                try:
                    year_asked = int(search_tuple[1])
                    if year_asked <= self.current_year:
                        search_tree = query_tree.find_npcs_by_category(search_tuple[0], search_tuple[1], search_tree)
                    else:
                        search_tree = []
                except ValueError:
                    search_tree = []
            else:
                exact = (search_tuple[0].lower() == "gender")
                search_tree = query_tree.find_npcs_by_category(search_tuple[0],
                                                               search_tuple[1],
                                                               search_tree,
                                                               exact=exact)
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
