import os
import config
from bot_identity.identity import Identity


DATA_DIR = os.path.sep.join([config.BASEDIR, "bot_identity", "data/"])

IDENTITY_FILES = ["identity1.xml", "identity2.xml"]
FACT_FILE = DATA_DIR + "facts.xml"

DEFAULT_ID = Identity(DATA_DIR + "default.xml", default=True)
GLOBAL_REGEX = {
    "(goe(d|i)emorgen|mogg(e|u))": "morning",
    "((wel)?te?ruste(n)?|slaap lekker|good night)": "night",
    "((bedankt|thank you|thanks|dank ?je ?(wel)?),? {})": "thanks",
}