

COLOR_HEARTS = ["❤", "💜", "💙", "💚", "💛"]
SPECIAL_HEARTS = ["♥", "❣", "💗", "💓", "💝", "💖", "💕", "💟",  "🖤"]


def is_heart_emoji(emoji):
    if emoji in COLOR_HEARTS or emoji in SPECIAL_HEARTS:
        return True
    return False


def get_heart_in_message(message):
    heart_list = []
    for heart in COLOR_HEARTS + SPECIAL_HEARTS:
        if heart in message:
            heart_list.append(heart)
    return heart_list
