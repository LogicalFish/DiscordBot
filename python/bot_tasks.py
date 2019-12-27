import discord
from discord.utils import get
import asyncio
import logging

import config

THIRD_DAY = 8*60*60
logger = logging.getLogger(__name__)

"""
Various methods that set up additional loops running in the background.
"""


async def calendar_task(client, system):
    """
    A separate thread, keeping track of tasks on the calendar.
    """
    await client.wait_until_ready()
    while not client.is_closed() and system.time_manager is not None:
        logger.debug("Checking the calendar for reminders.")
        reminders = system.time_manager.clock_pass()
        for date, reminder_embed, channel_name, tag_name in reminders:
            if len(channel_name):
                channels = filter(lambda ch: ch.name == channel_name, client.get_all_channels())
                for channel in channels:
                    if isinstance(channel, discord.TextChannel):
                        tag = get(channel.guild.roles, name=tag_name)
                        if tag:
                            message = config.localization['event_model']['reminder_tag'].format(tag.mention)
                            await channel.send(content=message, embed=reminder_embed)
                        else:
                            await channel.send(embed=reminder_embed)
        await asyncio.sleep(30)


async def birthday_task(client, system):
    """
    A separate thread, keeping track of birthdays.
    """
    await client.wait_until_ready()
    while not client.is_closed():
        logger.debug("Checking the Birthday Manager for birthdays.")
        birthday_ids = system.birthday_manager.get_today_birthdays()
        for birthday_id in birthday_ids:
            channels = get_main_channels(client)
            for channel in channels:
                birthday_user = system.get_user_by_id(birthday_id, client=client, guild=channel.guild)
                user_name = system.name_manager.get_name(birthday_user)
                message = system.id_manager.id_statement("general", "birthday").format(user_name)
                await channel.send(message)
        if birthday_ids:
            await asyncio.sleep(THIRD_DAY*2)
        await asyncio.sleep(THIRD_DAY)


async def reminder_task(client, system):

    """
    A separate thread, keeping track of reminders.
    """
    await client.wait_until_ready()
    while not client.is_closed() and system.reminder_manager is not None:
        logger.debug("Checking the Reminder Manager for reminders.")
        reminder_list = system.reminder_manager.get_all_reminders()
        for reminder in reminder_list:
            date, message, owner = reminder
            await owner.send(content=message)
        await asyncio.sleep(60)


def get_main_channels(client, system):
    main_channels = []
    for channel_name in system.configuration['birthdays']['channels']:
        named_channels = filter(lambda ch: ch.name == channel_name, client.get_all_channels())
        for channel in named_channels:
            if isinstance(channel, discord.TextChannel):
                main_channels.append(channel)
    return main_channels
