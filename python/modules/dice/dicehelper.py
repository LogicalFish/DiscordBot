import re
import operator

from . import dice_config as config



def string_to_dice_pairs(msg):
    """
    Method that takes a message string, and finds all dice notations and numbers mentioned in this message.
    :param msg: The string, possibly containing dice.
    :return: A list of tuples, each tuple having a length of two and representing dice notation.
    """
    # Catches all numbers of the format XdY and dY
    stringresult = re.findall("(-?\\s*\\d+)?d(\\d+)", msg)
    # Edge-case: Catches solitary numbers.
    stringresult += re.findall("((?:[+\\- ]|^)\\s*\\d+)(?!d|\\d)()", msg)
    result = []
    for sr in stringresult:
        x, y = sr
        x, y = [i.replace(" ", "") for i in [x, y]]
        x, y = ['1' if i == '' else i for i in [x, y]]
        if x != '0' and y != '0' and int(y) < config.MAXDIETYPE:
            result.append((int(x), int(y)))
    return result


def dice_pairs_to_string(dice_pairs):
    """
    A method that converts a list of tuples representing dice to a string.
    :param dice_pairs: A list of tuples, each tuple having a length of two and representing dice notation.
    :return: A string that represents the tuples.
    """
    result = ""
    for i, pair in enumerate(dice_pairs):
        x, y = pair
        if x >= 0 and i > 0:
            result += "+"
        result += "{}".format(x)
        if y > 1:
            result += "d{}".format(y)
    return result


def sort_dice(dice_pairs):
    """
    A method that sorts a list of dice-pairs and adds dice with the same amount of faces in the same notation.
    EXAMPLE: 1d20 + 1d8 + 1d12 + 1d20 => 2d20 + 1d12 + 1d8
    :param dice_pairs: A list of tuples, each tuple having a length of two and representing dice notation.
    :return: The input, sorted and compressed.
    """
    dice_pairs.sort(key=operator.itemgetter(1), reverse=True)
    i = 0
    while i+1 < len(dice_pairs):
        if dice_pairs[i+1][1] == dice_pairs[i][1] and dice_pairs[i+1][0]*dice_pairs[i][0] > 0:
            combination = (dice_pairs[i+1][0]+dice_pairs[i][0], dice_pairs[i][1])
            dice_pairs.pop(i)
            dice_pairs.pop(i)
            dice_pairs.insert(i, combination)
            i -= 1
        i += 1
    return dice_pairs


def prune_dice(dice_pairs):
    """
    A method that takes a list of dice-pairs, counts the amount of dice,
    and removes any dice-pairs that would put it over the cap.
    :param dice_pairs: A list of tuples, each tuple having a length of two and representing dice notation.
    :return: the pruned list, plus the final count of every dice.
    """
    pruned_dice = dice_pairs
    count = 0
    i = 0
    # for i, pair in enumerate(pruned_dice):
    while i < len(pruned_dice):
        x, y = pruned_dice[i]
        if y > 1:
            count += abs(x)
        if count > config.DHARDCAP:
            if i > 0:
                if y != 1:
                    pruned_dice.pop(i)
                    i -= 1
            else:
                pruned_dice[i] = (config.DHARDCAP, y)
        i += 1
    if len(pruned_dice) == 1 and pruned_dice[0][1] == 1:
        pruned_dice.pop(0)
    return pruned_dice


def get_dice_count(dice_pairs):
    count = 0
    for x, y in dice_pairs:
        if y > 1:
            count += abs(x)
    return count
