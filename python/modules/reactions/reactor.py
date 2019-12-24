import os
import re
import yaml

from config import configuration, BASEDIR

reactions = {}
if 'reactions_file' in configuration['dir']:
    reactions_file = os.path.sep.join([BASEDIR] + configuration['dir']['reactions_file'])
    if os.path.isfile(reactions_file):
        reactions = yaml.safe_load(open(reactions_file, encoding="utf8"))


def get_reaction_to_reaction(reaction):
    for category in reactions:
        if "emoji_triggers" in reactions[category] and reaction.emoji in reactions[category]["emoji_triggers"]:
            return {"react": [reaction.emoji]}
        elif "custom_emoji" in reactions[category]:
            custom_string = "<:{}:{}>".format(reactions[category]["custom_emoji"]["name"],
                                              reactions[category]["custom_emoji"]["id"])
            if str(reaction.emoji) == custom_string:
                return {"react": [reaction.emoji]}
    return {}


def get_reaction_to_message(message):
    response_list = []
    custom_response_list = []
    for category in reactions:
        if "emoji_triggers" in reactions[category]:
            for emoji in reactions[category]["emoji_triggers"]:
                if emoji in message.content:
                    response_list.append(emoji)
        if "text_triggers" in reactions[category]:
            matches = re.findall(reactions[category]["text_triggers"], message.content)
            if len(matches):
                if "emoji_response" in reactions[category]:
                    response_list += reactions[category]["emoji_response"]
                if "custom_emoji" in reactions[category]:
                    custom_response_list.append(reactions[category]["custom_emoji"]["name"])
    return response_list, custom_response_list
