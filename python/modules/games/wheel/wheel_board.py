import random
from xml.etree import ElementTree

from modules.games.wheel import wheel_config


class FortunateBoard:
    # UNICODE_AID = ord('🇦') - ord('a')
    FREE_SPACE = "⬜"
    HIDDEN = "⬛"

    def __init__(self):
        """
        Initializes the board by picking a random phrase.
        """
        self.word, self.category = self.get_random_word()
        self.revealed = []
        self.solved = False

    def __str__(self):
        hidden_word = ""
        for char in self.word:
            if char.isalpha():
                if char not in self.revealed and not self.solved:
                    hidden_word += self.HIDDEN
                else:
                    # hidden_word += chr(self.UNICODE_AID + ord(char))
                    hidden_word += ":regional_indicator_{}:".format(char)
            elif char.isspace():
                hidden_word += self.FREE_SPACE
            else:
                hidden_word += char
        return hidden_word

    def guess_consonant(self, guess):
        if not self.is_valid_character(guess):
            raise ValueError("invalid_character")
        if self.is_vowel(guess):
            raise ValueError("vowel")
        return self.reveal(guess)

    def buy_vowel(self, guess):
        if not self.is_valid_character(guess):
            raise ValueError("invalid_character")
        if not self.is_vowel(guess):
            raise ValueError("not_a_vowel")
        return self.reveal(guess)

    def reveal(self, char):
        if not self.is_revealed(char):
            self.revealed.append(char.lower())
            return self.word.count(char)
        # else:
        # raise ValueError("already_revealed")
        return 0

    def solve_word(self, guess):
        self.solved = guess.lower() == self.word
        return self.solved

    def is_revealed(self, char):
        return char.lower() in self.revealed

    @staticmethod
    def is_valid_character(char):
        return isinstance(char, str) and len(char) is 1 and char.isalpha()

    @staticmethod
    def is_vowel(char):
        if char in ('a', 'e', 'i', 'o', 'u'):
            return True
        return False

    @staticmethod
    def get_random_word():
        word_doc = ElementTree.parse(wheel_config.WORD_LIST).getroot()

        word_list = word_doc.findall("category/entry")
        chosen_entry = random.choice(word_list)
        category_name = "None"

        for category in word_doc.iter("category"):
            if chosen_entry in category.findall("entry"):
                category_name = category.attrib["name"]
                break

        return chosen_entry.text.lower(), category_name
