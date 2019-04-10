import os
from bot_identity.identity import Identity

#SECRET TOKEN, DO NOT SHARE
TOKEN = "[SECRET TOKEN GOES HERE]"

#Directories and Files
BASEDIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = BASEDIR + "/bot_identity/data/"

IDENTITY_FILES = ["default.xml"]
FACT_FILE = DATA_DIR + "facts.xml"

#COMMAND CHARACTER(S)
SIGN = '::'


#DICE SETTINGS:
DSOFTCAP = 20
DHARDCAP = 100
MAXDIETYPE = 1000

#DEFAULT IDENTITY SETTINGS:
DEFAULT_ID = Identity(DATA_DIR + "default.xml", default=True)
GLOBAL_REGEX = {
    "(goedemorgen|mogg(e|u))": "morning",
    "((wel)?te?ruste(n)?|slaap lekker|good night,? [bot])": "night",
    "((bedankt|thank you|thanks|dank ?je ?(wel)?),? [bot])": "thanks",
}
BOT = "[bot]"

#EVENT SETTINGS
MAX_EVENT_NAME = 25
MAX_EVENT_DESCRIPTION = 255
MAX_EVENTS = 10
MAX_INTERVAL = 365

#TIC-TAC-TOE SETTINGS:
#TOKENS:
TOKENS = ["❌", "⭕"]
FREE_SPACE = "⬜"

CANTON = "⬛"
DISPLAY_ROWS = ["1⃣","2⃣","3⃣"]
DISPLAY_COLUMNS = ["🇦","🇧","🇨"]
