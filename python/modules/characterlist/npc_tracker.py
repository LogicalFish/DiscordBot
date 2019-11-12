from xml.etree import ElementTree

from modules.characterlist import query_tree
from modules.characterlist.character_info import CharacterInfo


class NPCTracker:

    def __init__(self, name, file, owner, year, color):
        self.name = name
        self.owner = owner
        self.current_year = year
        self.root = ElementTree.parse(file).getroot()
        self.color = color

    def year_up(self, number=1):
        self.current_year += number

    def get_list_of_npcs(self, search_tuples):
        search_tree = self.root
        for search_tuple in search_tuples:
            if search_tuple[0].lower() == "list":
                if search_tuple[1].lower() != self.name.lower():
                    print(search_tuple[1])
                    print(self.name)
                    return []
            elif search_tuple[0].lower() == "any":
                search_tree = query_tree.find_npcs_by_any(search_tuple[1], search_tree)
            elif search_tuple[0].lower() == "name":
                search_tree, score = query_tree.find_npcs_by_name(search_tuple[1], search_tree)
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
        # final_list.sort(key=operator.attrgetter("sort_key", "secondary_sort_key"))
        return self.search_tree_to_list(search_tree)

    def get_npcs_by_name_only(self, param):
        search_tree, score = query_tree.find_npcs_by_name(param, self.root)
        final_list = self.search_tree_to_list(search_tree)
        return final_list, score

    def search_tree_to_list(self, search_tree):
        result = []
        for found_item in search_tree:
            npc = CharacterInfo(query_tree.item_to_dictionary(found_item), self.current_year, self.color)
            result.append(npc)
        return result
