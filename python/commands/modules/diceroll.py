import operator
import re
import random
import settings as s

"""
On Dice Notation:
A dice is shared in the following format: XdY, with X being the amount of dice, and Y the amount of sides the dice have.
For example, 8d6 means eight six-sided dice are rolled, while 1d20 is one twenty-sided dice.
If the X value is missing, a 1 is assumed. d12 <==> 1d12.
A single number X may also be added, in which case they are represented as Xd1 tuple in the code, and in the code only.
"""



def respond(message):
    """
    Parses a message, searching for dice input (XdY), and generates random numbers based on these.
    :param message: the original message, containing input parameters.
    :return: A string containing a summary and the outcome of the rolled dice.
    """
    response = ""
    inputarray = message.split("|")
    for input in inputarray:
        dice_pairs = string_to_dice_pairs(input)
        dice_pairs = combine_dice(dice_pairs)
        dice_pairs, count = prune_dice(dice_pairs)

        if len(dice_pairs) > 0:
            response += "You have asked to roll the following dice: {}.\n".format(dice_pairs_to_string(dice_pairs))

            response += "\tResult: "
            results = dice_roll(dice_pairs)

            if count < s.DSOFTCAP:
                for i, result in enumerate(results):
                    if result >= 0 and i > 0:
                        response += "+"
                    response += "{}".format(result)
                response+= " = "
            response += "**{}**.\n".format(sum(results))

            if count > s.DHARDCAP:
                response += "\nERROR: You rolled too many dice. The list of dice was pruned. The maximum is {}.\n".format(s.DHARDCAP)
        else:
            response = "ERROR: Did not read valid dice. Reminder: Any dice higher than a d{} are ignored.\n".format(s.MAXDIETYPE)

    return response


def string_to_dice_pairs(msg):
    """
    Method that takes a message string, and finds all dice notations and numbers mentioned in this message.
    :param msg: The string, possibly containing dice.
    :return: A list of tuples, each tuple having a length of two and representing dice notation.
    """
    # Catches all numbers of the format XdY and dY
    stringresult = re.findall("(-?\\s*\\d+)?d(\\d+)", msg)
    # Edge-case: Catches solitary numbers.
    stringresult += re.findall("((?:\\+|-| )\\s*\\d+)(?!d|\\d)()", msg)
    result = []
    for sr in stringresult:
        x, y = sr
        x, y = [i.replace(" ", "") for i in [x,y]]
        x, y = ['1' if i == '' else i for i in [x,y]]
        if x != '0' and y != '0' and int(y) < s.MAXDIETYPE:
            result.append((int(x),int(y)))
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


def dice_roll(dice_pairs):
    """
    A method that generates a random number based on a list of dice-pairs.
    :param dice_pairs: A list of tuples, each tuple having a length of two and representing dice notation.
    :return: A list containing a random number for each dice in the dice_pairs list.
    """
    results = []
    for pair in dice_pairs:
        x,y = pair
        signbit = -1 if x<0 else 1
        if 1 < y <= s.MAXDIETYPE and len(results) <= s.DHARDCAP:
            r = min(abs(x), s.DHARDCAP - len(results))
            for i in range(r):
                results.append(random.randint(1,y)*signbit)
        elif y == 1:
            results.append(x)
    return results


def combine_dice(dice_pairs):
    """
    A method that sorts a list of dice-pairs and adds dice with the same amount of faces in the same notation.
    EXAMPLE: 1d20 + 1d8 + 1d12 + 1d20 => 2d20 + 1d12 + 1d8
    :param dice_pairs: A list of tuples, each tuple having a length of two and representing dice notation.
    :return: The input, sorted and compressed.
    """
    result = dice_pairs
    result.sort(key=operator.itemgetter(1), reverse=True)
    i = 0
    while i+1 < len(result):
        if result[i+1][1] == result[i][1] and result[i+1][0]*result[i][0] > 0:
            combination = (result[i+1][0]+result[i][0], result[i][1])
            result.pop(i)
            result.pop(i)
            result.insert(i, combination)
            i -= 1
        i += 1
    return result


def prune_dice(dice_pairs):
    """
    A method that takes a list of dice-pairs, counts the amount of dice, and removes any dice-pairs that would put it over the cap.
    :param dice_pairs: A list of tuples, each tuple having a length of two and representing dice notation.
    :return: the pruned list, plus the final count of every dice.
    """
    result = dice_pairs
    count = 0
    for i, pair in enumerate(result):
        x,y = pair
        if y > 1: count += abs(x)
        if count > s.DHARDCAP and i > 0:
            while i < len(result):
                if result[i][1] != 1:
                    result.pop(i)
                else:
                    i+=1
        elif count > s.DHARDCAP:
            result[i] = (s.DHARDCAP, result[i][1])
    if len(result) == 1 and result[0][1] == 1:
        result.pop(0)
    return result, count
