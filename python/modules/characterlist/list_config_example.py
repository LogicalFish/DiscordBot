import os
import config

DATA_DIR = os.path.sep.join([config.BASEDIR, "modules", "characterlist", "data"])
NPC_LIST = os.path.sep.join([DATA_DIR, "NPCs.xml"])

SETTING_NAME = "Setting" # Insert your own name here.
OWNER_ID = -1  # Insert your own ID here.
BASE_YEAR = 2000  # Insert the current year here.
COLOR = int("000000", 16)

NPC_TUPLE = (SETTING_NAME, NPC_LIST, OWNER_ID, BASE_YEAR, COLOR)

NPC_LISTS = [NPC_TUPLE]