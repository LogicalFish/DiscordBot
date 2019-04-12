import discord
from discord.utils import get
import asyncio


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
