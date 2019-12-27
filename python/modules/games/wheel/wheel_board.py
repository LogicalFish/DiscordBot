import os
import yaml
import random

from config import configuration, BASEDIR
display_config = configuration['wheel']['display']


class WheelBoard:

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
                    hidden_word += display_config['hidden']
                else:
                    hidden_word += display_config['letter'].format(char)
            elif char in display_config['punctuation']:
                hidden_word += display_config['punctuation'][char]
            elif char.isspace():
                hidden_word += display_config['space']
            # else:
            #     hidden_word += char
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
        if char.lower() in ('a', 'e', 'i', 'o', 'u'):
            return True
        return False

    @staticmethod
    def get_random_word():
        word_file = os.path.sep.join([BASEDIR] + configuration['wheel']['words_file'])
        word_doc = yaml.safe_load(open(word_file))

        categories = list(word_doc.keys())
        cat_weights = [len(word_doc[cat]) for cat in categories]

        random_category = random.choices(categories, weights=cat_weights)[0]

        random_word = random.choice(word_doc[random_category])

        return random_word.lower(), random_category
