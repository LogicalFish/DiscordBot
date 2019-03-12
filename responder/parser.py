import re
import random
from responder.identity import IdentityError
from responder import facts
import settings


def find_new_id(message, id_list):
    """
    Method that goes through a message to find all identities that are mentioned within.

    :param message: The message sent by a user.
    :param id_list: The list of all Identities.
    :return: A list containing all the identities that have been mentioned in the text.
    """
    result = []
    for identity in id_list:
       try:
            matches = re.findall(identity.get_regex().lower(), message.lower())
            if len(matches):
                result.append(identity)
       except IdentityError as ie:
           print("IdentityError: {} Skipping identity.".format(ie))
    return result


def get_default_dict(identity):
    """
    Returns the Global Regex values from settings.py, with the identity names inserted.
    :param identity: The identity to be inserted.
    :return: A dictionary containing all default regular expressions
    """
    result = {}
    for value in settings.GLOBAL_REGEX:
        result[value.replace(settings.BOT, identity.get_regex())] = settings.GLOBAL_REGEX[value]
    return result


def get_response(message, identity):
    """
    Searches through a message and returns and phrases specific to the supplied identity
    :param message: The message to be searched through.
    :param identity: The identity defining the search parameters. (Usually the current one)
    :return: A random response based on the message, or an empty string if none could be found.
    """
    # Step 1: Get dictionary of all responses.
    default_dict = get_default_dict(identity)
    special_dict = identity.special_list()
    fact_dict = facts.get_listdict()

    full_dict = {**default_dict,**special_dict,**fact_dict}

    for regex in full_dict:
        matches = re.findall(regex.lower(), message.lower())
        if len(matches):
            if regex in fact_dict:
                response_list = facts.get_fact_list(fact_dict[regex])
            else:
                response_list = identity.phrase_list(full_dict[regex])
            if len(response_list) == 0:
                if regex in default_dict:
                    response_list = settings.DEFAULT_ID.phrase_list(default_dict[regex])
                else:
                    return ""
            return random.choice(response_list)
    return ""


def direct_call(identity, tag):
    """
    A method that will directly retrieve a random element with a specified tag.
    If no elements are found with that tag, the default one is used.
    :param identity: The identity to check for the tag. (Usually the current one)
    :param tag: The specific tag you are looking for.
    :return: A random response based on the supplied tag.
    """
    response_list = identity.phrase_list(tag)
    if len(response_list) == 0:
        response_list = settings.DEFAULT_ID.phrase_list(tag)
    return random.choice(response_list)

