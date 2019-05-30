import os

# SECRET TOKEN, DO NOT SHARE
TOKEN = "[SECRET TOKEN GOES HERE]"

# COMMAND CHARACTER(S)
SIGN = '!'

CHARACTER_MAX = 2000

# Directories and Files
BASEDIR = os.path.dirname(os.path.abspath(__file__))
DB_INI = os.path.sep.join([BASEDIR, "database", "database.ini"])
