
RACCOON_EMOJI_NAME = "WAT"
EMOJI_ID = 539759475930955787
RACCOON_EMOJI = "🦝"

raccoon_words = ["raccoon", "wasbeer", "wasberen", "watbeer"]


def is_raccoon_emoji(emoji):
    if str(emoji) == "<:{}:{}>".format(RACCOON_EMOJI_NAME, EMOJI_ID) or emoji == RACCOON_EMOJI:
        return True
    return False


def contains_racoons(message):
    if "WAT" in message:
        return True
    for word in raccoon_words:
        if word in message.lower():
            return True
    return False

