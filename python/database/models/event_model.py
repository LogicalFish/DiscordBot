import copy

import discord
from datetime import timedelta
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, ARRAY
from database.database_connection import Base
from modules.calendar import event_parser, calendar_config


class Event(Base):
    __tablename__ = 'events'

    event_id = Column('event_id', Integer, primary_key=True)
    name = Column('name', String(calendar_config.MAX_EVENT_NAME))
    date = Column('date', DateTime)
    author = Column('author', BigInteger)

    description = Column('description', String(calendar_config.MAX_EVENT_DESCRIPTION), nullable=True)
    channel = Column('channel', String(255), nullable=True)
    tag = Column('tag', String(255), nullable=True)
    reminder = Column('reminder', ARRAY(Integer), nullable=True)
    recur = Column('recur', Integer, nullable=True)

    def __init__(self, name, date, author, description="", channel=None, tag=None, reminder=None, recur=None, **kwargs):
        self.author = author
        self.update(name, date, description, channel, tag, reminder, recur)

    def update(self, name=None, date=None, description=None, channel=None, tag=None, reminder=None, recur=None, **kwargs):
        if name:
            self.name = event_parser.parse_string(name, calendar_config.MAX_EVENT_NAME, "name")
        if date:
            self.date = event_parser.parse_date(date)
        if description:
            self.description = event_parser.parse_string(description, calendar_config.MAX_EVENT_DESCRIPTION,
                                                         "description")
        if channel:
            self.channel = event_parser.parse_string(channel, 255, "channel")
        if tag:
            self.tag = event_parser.parse_string(tag, 255, "tag")
        if reminder:
            self.reminder = event_parser.parse_int_array(reminder)
        if recur:
            self.recur = event_parser.parse_integer(recur)

    def recur_self(self):
        if self.recur:
            next_time = timedelta(days=self.recur)
            self.date = self.date + next_time

    def get_reminders(self):
        result = []
        if self.reminder:
            reminder_list = sorted(self.reminder, reverse=True)
            for hours in reminder_list:
                embed = self.describe_reminder(hours)
                reminder_time = self.date - timedelta(hours=hours)
                result.append((reminder_time, embed))
        return result

    def get_shadow_events(self, quantity):
        """
        Method to get a list of shadow events.
        :param quantity: The amount of shadow events you want, up to a maximum set in settings.
        :return: A list of shadow events
        """
        shadow_events = []
        if self.recur is not None:
            new_event = copy.deepcopy(self)
            shadow_time = timedelta(days=self.recur)
            for i in range(min(quantity, calendar_config.MAX_SHADOW)):
                new_event.date = new_event.date + shadow_time
                new_event.event_id = "{}-{}".format(self.event_id, (i+1))
                shadow_events.append(new_event)
                new_event = copy.deepcopy(new_event)
        return shadow_events

    def get_event_embed(self):
        embed = discord.Embed(title=self.name, description=self.description, color=13138175)
        embed.add_field(name="Date", value=self.date.strftime(calendar_config.DATE_FORMAT), inline=True)
        embed.add_field(name="Time", value=self.date.strftime(calendar_config.TIME_FORMAT), inline=True)
        reminders = self.embed_reminder_in_event()
        if len(reminders):
            embed.add_field(name="Reminders", value=reminders, inline=False)
        embed.set_footer(text="ID: {} ● Author: ".format(self.event_id))
        return embed

    def embed_reminder_in_event(self):
        result = ""
        if self.reminder:
            reminder_list = sorted(self.reminder, reverse=True)
            reminders = [str(d) for d in reminder_list]
            result += "h, ".join(reminders)
            result += "h in advance.\n"
        if self.channel:
            result += "Channel: #{}\n".format(self.channel)
        if self.tag:
            result += "Mention: @{}\n".format(self.tag)
        return result

    def describe_short(self):
        description = "**●** {} - **Event {}:** {}.\n".format(self.display_date(self.date), self.event_id, self.name)
        return description

    def describe_shadow(self):
        description = "*● {} - Event {}: {}.*\n".format(self.display_date(self.date), self.event_id, self.name)
        return description

    @staticmethod
    def display_date(datetime):
        return datetime.strftime("{}, {}".format(calendar_config.DATE_FORMAT, calendar_config.TIME_FORMAT))

    def describe_reminder(self, hours):
        hours_s = "s"
        if hours == 1:
            hours_s = ""
        reminder_description = "{} starts in {} hour{}!\n\n*{}*".format(self.name, hours, hours_s, self.description)
        reminder_embed = discord.Embed(title=self.name, description=reminder_description, color=13138175)
        reminder_embed.set_footer(text="ID: {}".format(self.event_id))

        return reminder_embed
