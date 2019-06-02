from xml.etree import ElementTree
from modules.characterlist import list_config

root = ElementTree.parse(list_config.NPC_LIST).getroot()


def item_to_dictionary(npc_item):
    npc_list_dict = {}
    for item in npc_item:
        if list(item):
            to_add = item_to_dictionary(item)
        else:
            to_add = item.text
        if item.tag in npc_list_dict:
            if type(npc_list_dict[item.tag]) == list:
                npc_list_dict[item.tag].append(to_add)
            else:
                npc_list_dict[item.tag] = [npc_list_dict[item.tag], to_add]
        else:
            npc_list_dict[item.tag] = to_add
    return npc_list_dict


def find_npcs_by_name(name, search_list=root):
    subnames = name.split()
    high_score = 0
    found_npcs = []
    for npc in search_list:
        score = 0
        for name_item in npc.find('names'):
            for name_sought in subnames:
                if name_item.tag != "title" and name_sought.lower() in name_item.text.lower():
                    score += 1
        if score > high_score:
            high_score = score
            found_npcs = []
        if score == high_score:
            found_npcs.append(npc)
    if high_score > 0:
        return found_npcs
    else:
        return []


def find_npcs_by_category(category, search_term, search_list=root):
    subcategories = category.split(".")
    found_npcs = []
    for npc in search_list:
        nodes = [npc]
        for sub in subcategories:
            nested_nodes = []
            for node in nodes:
                nested_nodes += node.findall(sub)
            nodes = nested_nodes
        for node in nodes:
            if search_term.lower() in node.text.lower():
                found_npcs.append(npc)
                break

    return found_npcs


def filter_living_npcs(year, search_list=root, death=False):
    valid_npcs = []
    for npc in search_list:
        deathyear_node = npc.find('deathyear')
        if deathyear_node is not None:
            death_year = int(deathyear_node.text)
            if year < death_year and not death:
                valid_npcs.append(npc)
            elif death and year > death_year:
                valid_npcs.append(npc)
        elif not death:
            valid_npcs.append(npc)
    return valid_npcs
