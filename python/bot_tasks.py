import discord
from discord.utils import get
import asyncio

from bot_identity import parser

THIRD_DAY = 8*60*60
main_channel_names = ["main", "general"]


async def calendar_task(client, system):
    """
    A separate thread, keeping track of tasks on the calendar.
    """
    await client.wait_until_ready()
    while not client.is_closed():
        reminders = system.time_manager.clock_pass()
        for date, reminder_embed, channel_name, tag_name in reminders:
            if len(channel_name):
                channels = filter(lambda ch: ch.name == channel_name, client.get_all_channels())
                for channel in channels:
                    if isinstance(channel, discord.TextChannel):
                        tag = get(channel.guild.roles, name=tag_name)
                        message = ""
                        if tag:
                            message = "Reminder for {}!:".format(tag.mention)
                        await channel.send(message, embed=reminder_embed)
        await asyncio.sleep(30)


async def birthday_task(client, system):
    await client.wait_until_ready()
    while not client.is_closed():
        birthday_ids = system.birthday_manager.get_today_birthdays()
        for birthday_id in birthday_ids:
            channels = get_main_channels(client)
            for channel in channels:
                birthday_name = system.nickname_manager.get_name_from_id(birthday_id, client, channel.guild)
                message = parser.direct_call(system.id_manager.current_id, "birthday").format(birthday_name)
                await channel.send(message)
                await asyncio.sleep(THIRD_DAY*2)
        await asyncio.sleep(THIRD_DAY)


def get_main_channels(client):
    main_channels = []
    for channel_name in main_channel_names:
        named_channels = filter(lambda ch: ch.name == channel_name, client.get_all_channels())
        for channel in named_channels:
            if isinstance(channel, discord.TextChannel):
                main_channels.append(channel)
    return main_channels
