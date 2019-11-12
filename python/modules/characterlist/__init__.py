from modules.characterlist import list_config
from modules.characterlist.npc_tracker import NPCTracker

npc_trackers = []
for args in list_config.NPC_LISTS:
    npc_trackers.append(NPCTracker(args[0], args[1], args[2], args[3], args[4]))

