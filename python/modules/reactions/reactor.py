from modules.reactions.heartful import is_heart_emoji


def get_reaction(reaction, user, system):
    if is_heart_emoji(reaction.emoji):
        return {"react": [reaction.emoji]}
    return {}
