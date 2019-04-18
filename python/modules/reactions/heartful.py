

COLOR_HEARTS = ["❤", "💜", "💙", "💚", "💛"]
SPECIAL_HEARTS = ["♥", "❣", "💗", "💓", "💝", "💖", "💕", "💟",  "🖤"]


def is_heart_emoji(emoji):
    """
    Method that checks if an emoji is a heart emoji.
    :param emoji: An emoji.
    :return: True if the emoji is a heart emoji. False if it is not.
    """
    if emoji in COLOR_HEARTS or emoji in SPECIAL_HEARTS:
        return True
    return False


def get_heart_in_message(message):
    """
    Method that checks if the message contains a heart.
    :param message: String: A message.
    :return: A list of heart emojis the message contains.
    """
    heart_list = []
    for heart in COLOR_HEARTS + SPECIAL_HEARTS:
        if heart in message:
            heart_list.append(heart)
    return heart_list
