import discord
from discord.ext import commands, tasks
from discord.utils import get
import pytz
import json
import datetime
import os
from models import ScheduleEventRequest as sched
import asyncio
import logging

logger = logging.getLogger('discord')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
bot = commands.Bot(intents=intents, command_prefix = '.')

@bot.event
async def createEvent(guild, event):
    """
    This method takes a dictionary named event,
    pulls event data from it,
    calculate what time corresponds to the next day of the week the event is scheduled for,
    and formats a request to create a scheduled event
    """

    for event in bot.data["eventList"]:
        event_name = event["name"]
        event_description = event["description"]
        eventStartTimeHours = event["startTime"]["hour"]
        eventStartTimeMinutes = event["startTime"]["minute"]
    
        # Get the current time in UTC.
        utc_now = pytz.utc.localize(datetime.datetime.now())

        # Calculate the start and end times of the next event.
        dayOfWeek = datetime.datetime.now(pytz.timezone("America/New_York")).weekday()
        daysUntilMonday = (7 - dayOfWeek) % 7
        nextMonday = datetime.timedelta(days=daysUntilMonday) + datetime.datetime.now(pytz.timezone("America/New_York"))
        nextMonday = nextMonday.replace(hour=eventStartTimeHours, minute=eventStartTimeMinutes, second=0)

        next_event_start = nextMonday
        next_event_end = next_event_start + datetime.timedelta(hours=1)

        event_to_create = sched(
            name=event_name,
            description=event_description,
            start_time=next_event_start,
            end_time=next_event_end,
            entity_type=discord.EntiyType.external,
            location= "",
            privacy_level= discord.PrivacyLevel.guild_only
        )

        await guild.create_scheduled_event(**event_to_create)

@bot.event
async def checkEventExists(guild, event):
    """
    Checks all existing events in the server and see if any of there names match the event that is attempting to be created. Returns true if yes and false if no
    """

    existingEvents = await guild.fetch_scheduled_events()
    for existingEvent in existingEvents:
        if existingEvent.name == event["name"]:
            return True
    else:
        return False

@tasks.loop(hours=24)
async def eventTask():
    guild = bot.get_guild(bot.guildId)
    eventList = bot.data["eventList"]

    for event in eventList:
        eventExists = await checkEventExists(guild, event)
        if eventExists:
            logger.info(f"Event Name: {event['name']} already exists")
            continue
        
        await createEvent(guild, event)

@bot.event
async def on_ready():
    """
    Starts the eventTask and runs it every 24 hours
    """
    logger.info(f"We have logged in as {bot.user}")
    eventTask.start()

# Start the bot.
def run():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    jsonFile = os.path.join(script_dir, "botConfig.json")

    with open(jsonFile, "r") as f:
        data = json.load(f)

        # Define the event name and description.
        token = data["token"]
        bot.guildId = data["guildId"]
        bot.data = data

        bot.run(token)
    f.close()