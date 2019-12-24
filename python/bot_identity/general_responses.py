import os

import yaml
import random


class GeneralResponder:

    def __init__(self, file_path):
        self.document = yaml.safe_load(open(os.path.sep.join(file_path)))

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
