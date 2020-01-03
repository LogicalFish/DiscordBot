import os
import yaml
import random

from config import configuration, BASEDIR
id_config = configuration['identity']

# Difficulty Translation Table
DIF = id_config['difficulty_table']


class Identity:
    """
    This class defines an Identity based on an XML document.
    Each Identity contains a multitude of elements divided amongst categories.
    Each element contains possible dialogue for any bot that is using this identity.
    """

    def __init__(self, file_path, default=False):
        self.document = yaml.safe_load(open(os.path.sep.join([BASEDIR] + file_path)))
        if not default:
            if "name" not in self.document or "regex" not in self.document:
                raise IdentityError("Could not create identity. Name or regex fields are missing.")
            self.name = self.document["name"]
            self.regex = "\\b{}\\b".format(self.document["regex"])

    def __str__(self):
        return self.name

    def get_game(self):
        """Returns the value of the game tag, or an empty string if no game-tag is found."""
        return self.document.get("game", "")

    def get_ai(self):
        """
        Returns the Difficulty of this identity within games.
        If the value is not within the DIF dictionary or an integer, the default is 3.
        :return: Integer representing difficulty
        """
        ai = self.document.get("AI", id_config['default_difficulty'])
        if isinstance(ai, int):
            return ai
        difficulty = ai.lower()
        try:
            return int(difficulty)
        except ValueError:
            return DIF.get(difficulty, id_config['default_difficulty'])

    def get_phrase(self, category, tag):
        if category in self.document and tag in self.document[category]:
            if category == "unique":
                phrasebook = self.document[category][tag]["response"]
            else:
                phrasebook = self.document[category][tag]
            if isinstance(phrasebook, list):
                return random.choice(phrasebook)
            else:
                return phrasebook
        else:
            return None

    def get_unique_triggers(self):
        """Returns the list of tags unique to the identity, and associated regex attributes."""
        result = {}
        if "unique" not in self.document:
            return result
        for key in self.document["unique"]:
            entry = self.document["unique"][key]
            if "regex" in entry and "response" in entry:
                result[key] = "\\b{}\\b".format(entry["regex"])
        return result


class IdentityError(Exception):
    """
    Special Error Class, to be thrown when an Identity is not initialized correctly.
    """

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return str(self.message)
