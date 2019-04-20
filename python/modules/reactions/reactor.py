from modules.reactions import heartful, watbeer


def get_reaction_to_reaction(reaction):
    """
    Method for determining if an emoji reaction should be reacted to by an emoji.
    :param reaction: The reaction.
    :return: An Action array. (See Bot Response Unit)
    """
    if heartful.is_heart_emoji(reaction.emoji):
        return {"react": [reaction.emoji]}
    if watbeer.is_raccoon_emoji(reaction.emoji):
        return {"react": [reaction.emoji]}
    return {}


def get_reaction_to_message(message):
    """
    Method for determining if a message should be reacted to.
    :param message: The message.
    :return: An Action array. (See Bot Response Unit)
    """
    reaction = heartful.get_heart_in_message(message.content)
    custom_reaction = watbeer.check_for_raccoon(message.content)
    return reaction, custom_reaction