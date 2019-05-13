import discord

from . import calendar_config as config

"""
Script for taking event data, and returning them in human-readable, easy to parse, form.
"""


def display_date(datetime):
    return datetime.strftime("{}, {}".format(config.DATE_FORMAT, config.TIME_FORMAT))


def describe_short(event):
    description = "**●** {} - **Event {}:** {}.\n".format(display_date(event["date"]), event["event_id"], event["name"])
    return description


def describe_shadow(event):
    description = "*● {} - Event {}: {}.*\n".format(display_date(event["date"]), event["event_id"], event["name"])
    return description


def get_reveal_message(shadow_event_id, new_event_id):
    return "Schaduw Evenement {} is nu evenement {}.".format(shadow_event_id, new_event_id)


def get_event_embed(event):
    embed = discord.Embed(title=event["name"], description=event["description"], color=13138175)
    embed.add_field(name="Date", value=event["date"].strftime(config.DATE_FORMAT), inline=True)
    embed.add_field(name="Time", value=event["date"].strftime(config.TIME_FORMAT), inline=True)
    embed.add_field(name="Reminders", value=embed_reminder_in_event(event), inline=False)
    embed.set_footer(text="ID: {} ● Author: ".format(event["event_id"]))
    return embed


def embed_reminder_in_event(event):
    result = ""
    if event["reminder"]:
        reminder_list = sorted(event["reminder"], reverse=True)
        for reminder in reminder_list:
            if result:
                result += ", "
            result += "{}h".format(reminder)
        result += " in advance.\n"
    if event["channel"]:
        result += "Channel: #{}\n".format(event["channel"])
    if event["tag"]:
        result += "Mention: @{}\n".format(event["tag"])
    return result


def describe_reminder(event, hours):
    hours_s = "s"
    if hours == 1:
        hours_s = ""
    reminder_description = "{} starts in {} hour{}!\n\n*{}*".format(event["name"],
                                                                    hours,
                                                                    hours_s,
                                                                    event["description"])
    reminder_embed = discord.Embed(title=event["name"], description=reminder_description, color=13138175)
    reminder_embed.set_footer(text="ID: {}".format(event["event_id"]))

    return reminder_embed

