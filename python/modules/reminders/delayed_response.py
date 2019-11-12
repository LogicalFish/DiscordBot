import re
import random

from datetime import timedelta

from discord import GroupChannel

delayed_messages = [("mechani.*(toetsenbord|keyboard)", "Mechanische toetsenborden zijn cool!")]


def add_reminder_if_trigger(message, system):
    for delay in delayed_messages:
        matches = re.findall(delay[0].lower(), message.content.lower())
        if len(matches):
            system.reminder_manager.add_reminder(get_random_waiting_period(), delay[1], get_user(message))
    return False


def get_user(message):
    if isinstance(message.channel, GroupChannel):
        return message.channel
    else:
        return message.author


def get_random_waiting_period():
    rnd = random.randint(3, 8)
    return timedelta(hours=rnd)
