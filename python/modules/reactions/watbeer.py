
RACCOON_EMOJI_NAME = "WAT"
EMOJI_ID = 539759475930955787

raccoon_words = ["raccoon", "wasbeer", "wasberen", "watbeer"]


def is_raccoon_emoji(emoji):
    if str(emoji) == "<:{}:{}>".format(RACCOON_EMOJI_NAME, EMOJI_ID):
        return True
    return False


def check_for_raccoon(message):
    if RACCOON_EMOJI_NAME in message:
        return [RACCOON_EMOJI_NAME]
    for word in raccoon_words:
        if word in message.lower():
            return [RACCOON_EMOJI_NAME]
    return []
