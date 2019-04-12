from modules.reactions import heartful, watbeer


def get_reaction_to_reaction(reaction):
    if heartful.is_heart_emoji(reaction.emoji):
        return {"react": [reaction.emoji]}
    if watbeer.is_raccoon_emoji(reaction.emoji):
        return {"react": [reaction.emoji]}

    return {}


def get_reaction_to_message(message):
    reaction = heartful.get_heart_in_message(message.content)
    custom_reaction = watbeer.check_for_raccoon(message.content)
    return reaction, custom_reaction
