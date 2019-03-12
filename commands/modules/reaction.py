import emoji
import re


def findEmojis(message):
    """
    Find all emojis within a message.
    :param message: The message to be searched.
    :return: A list of found emojis (in emoji form)
    """
    result = re.findall(emoji.get_emoji_regexp(), message)
    return result

def findCustomEmojis(message):
    """
    Find all custom emojis within a message.
    :param message: The message to be searched.
    :return: A list of names of found emojis.
    """
    custom = re.findall("<:(\w+):\d+>", message)
    return custom
