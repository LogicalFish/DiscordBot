import os
import yaml
import random

from config import configuration

fact_file = os.path.sep.join(configuration['identity']['identity_dir'] + [configuration['identity']['facts_file']])
document = yaml.safe_load(open(fact_file))


def get_random_fact(subject):
    if subject in document:
        return random.choice(document[subject]["response"])
    return None


def get_triggers():
    """Returns the list of tags unique to the identity, and associated regex attributes."""
    result = {}
    for key in document:
        if "regex" in document[key] and "response" in document[key]:
            result[key] = document[key]["regex"]
    return result
