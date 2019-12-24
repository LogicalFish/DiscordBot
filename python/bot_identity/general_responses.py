import os
import yaml
import random
from config import BASEDIR


class GeneralResponder:

    def __init__(self, file_path):
        file_name = os.path.sep.join([BASEDIR] + file_path)
        if os.path.isfile(file_name):
            self.document = yaml.safe_load(open(file_name))
        else:
            print("No General Response File Found. Skipping Load")
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
