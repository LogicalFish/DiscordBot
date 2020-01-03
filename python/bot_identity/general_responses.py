import os
import yaml
import random
import logging
from config import BASEDIR

logger = logging.getLogger(__name__)


class GeneralResponder:

    def __init__(self, file_path):
        file_name = os.path.sep.join([BASEDIR] + file_path)
        if os.path.isfile(file_name):
            self.document = yaml.safe_load(open(file_name))
        else:
            logging.warning("No general response file found. No responses has been loaded.")
            self.document = []

    def get_random_fact(self, subject, message):
        if subject in self.document:
            return random.choice(self.document[subject]["response"])
        return None

    def get_triggers(self):
        """Returns the list of tags unique to the identity, and associated regex attributes."""
        result = {}
        for key in self.document:
            entry = self.document[key]
            if "regex" in entry and "response" in entry:
                result[key] = entry["regex"]
        return result
