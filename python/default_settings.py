import os
from bot_identity.identity import Identity

# SECRET TOKEN, DO NOT SHARE
TOKEN = "[SECRET TOKEN GOES HERE]"

# Directories and Files
BASEDIR = os.path.dirname(os.path.abspath(__file__))
XML_DIR = BASEDIR + "/bot_identity/data/"
DB_INI = BASEDIR + '/database/database.ini'

# IDENTITY FILES
IDENTITY_FILES = ["default.xml"]
FACT_FILE = XML_DIR + "facts.xml"

# COMMAND CHARACTER(S)
SIGN = '!!'

# NICKNAME SETTINGS
MAX_NICK_NAME = 50

# DICE SETTINGS:
DSOFTCAP = 20
DHARDCAP = 100
MAXDIETYPE = 1000

# DEFAULT IDENTITY SETTINGS:
DEFAULT_ID = Identity(XML_DIR + "default.xml", default=True)
GLOBAL_REGEX = {
    "(goe(d|i)emorgen|mogg(e|u))": "morning",
    "((wel)?te?ruste(n)?|slaap lekker|good night,? [bot])": "night",
    "((bedankt|thank you|thanks|dank ?je ?(wel)?),? [bot])": "thanks",
}
BOT = "[bot]"

# EVENT SETTINGS
MAX_EVENT_NAME = 25
MAX_EVENT_DESCRIPTION = 255
MAX_EVENTS = 10
MAX_INTERVAL = 365

DATE_FORMAT = "%a %d %B, %Y"
TIME_FORMAT = "%H:%M"

# SHADOW EVENT SETTINGS
MAX_SHADOW = 9
DEFAULT_SHADOW = 3

# TIC-TAC-TOE SETTINGS:
TTT_PIECES = ["❌", "⭕"]
FREE_SPACE = "⬜"

CANTON = "⬛"
DISPLAY_ROWS = ["1⃣", "2⃣", "3⃣"]
DISPLAY_COLUMNS = ["🇦", "🇧", "🇨"]

# MINESWEEPER:
SWEEPER_MINE = "💣"
SWEEPER_NUMBERS = ["⬜", "1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣"]

SWEEPER_MAX_SIZE = 198
SWEEPER_AI_TABLE = {1: (6, 4), 2: (8, 6), 3: (12, 8), 4: (14, 10), 5: (18, 11)}
SWEEPER_AI_BOMBS = {1: 1, 2: 5, 3: 14, 4: 25, 5: 40}
