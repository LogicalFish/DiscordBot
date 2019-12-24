import os

from config import configuration, BASEDIR
from modules.characterlist.npc_tracker import NPCTracker

data_dir = os.path.sep.join([BASEDIR] + configuration['character_list']['list_dir'])
npc_trackers = []

for char_list in configuration['character_list']['lists']:
    details = configuration['character_list'][char_list]
    npc_trackers.append(NPCTracker(name=str(char_list).title(),
                                   file=os.path.sep.join([data_dir, details['file']]),
                                   owner=details['owner'],
                                   year=details['default_year'],
                                   color=int(details['color'], 16)))

