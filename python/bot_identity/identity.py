import os
from xml.etree import ElementTree

from config import configuration
id_config = configuration['identity']

# Special tags used in XML documents.
TAG = id_config['xml_tags']

# Difficulty Translation Table
DIF = id_config['difficulty']


class Identity:
    """
    This class defines an Identity based on an XML document.
    Each Identity contains a multitude of elements divided amongst categories.
    Each element contains possible dialogue for any bot that is using this identity.
    """

    def __init__(self, file_name, default=False):
        file_location = os.path.sep.join(id_config['identity_dir'] + [file_name])
        self.root = ElementTree.parse(file_location).getroot()
        if not default:
            try:
                # Check if the identity has a name and regex field. Throw an error if it doesn't.
                self.get_name()
                self.get_regex()
            except IdentityError as ie:
                raise IdentityError("Can not create identity. {}".format(ie))

    def get_name(self):
        """Return the value in the name tag. Returns an error if no name-tags are found."""
        e = self.root.find(TAG["NAME"])
        if e is not None:
            return e.text
        else:
            raise IdentityError("Missing <name> field.")

    def get_regex(self):
        """Return the regex attribute of the name tag. Returns an error if no regex attribute is found."""
        child = self.root.find(TAG["NAME"])
        if TAG["REGEX"] in child.attrib:
            return "\\b{}\\b".format(child.attrib[TAG["REGEX"]])
        else:
            raise IdentityError("Did not find a regex attribute in <name>.")

    def get_game(self):
        """Returns the value of the game tag, or an empty string if no game-tag is found."""
        e = self.root.find(TAG["GAME"])
        if e is not None:
            return e.text
        return ""

    def get_AI(self):
        """
        Returns the Difficulty of this identity within games.
        If the value is not within the DIF dictionary or an integer, the default is 3.
        :return: Integer representing difficulty
        """
        e = self.root.find(TAG["AI"])
        if e is not None:
            difficulty = e.text.lower()
            try:
                return int(difficulty)
            except ValueError:
                return DIF.get(difficulty, 3)
        return 3

    def phrase_list(self, tag):
        """Returns the list of elements within a specific tag."""
        phrases = []
        for child in self.root.iter(tag):
            for e in child.findall((TAG["ITEM"])):
                phrases.append(e.text)
        return phrases

    def special_list(self):
        """Returns the list of tags unique to the identity, and associated regex attributes."""
        result = {}
        for child in self.root.iter(TAG["SPEC"]):
            for grandchild in child:
                if TAG["REGEX"] in grandchild.attrib:
                    result[grandchild.attrib[TAG["REGEX"]]] = grandchild.tag

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
