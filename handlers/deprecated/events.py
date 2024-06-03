import discord
from discord.ext import commands, tasks
from discord.utils import get
import pytz
import datetime
import logging
from resources.models import ScheduleEventRequest as sched

logger = logging.getLogger('discord')

intents = discord.Intents.default()
bot = commands.Bot(intents=intents, command_prefix = '.')

@bot.event
async def createEvent(guild, event, userSubmitted=False):
    """
    This method takes a dictionary named event,
    pulls event data from it,
    calculate what time corresponds to the next day of the week the event is scheduled for,
    and formats a request to create a scheduled event
    """

    if userSubmitted:
        make(event)
    else:
        for event in bot.data["eventList"]:
            make(event)

    async def make(event):
        event_name = event["name"]
        event_description = event["description"]
        eventStartTimeHours = event["startTime"]["hour"]
        eventStartTimeMinutes = event["startTime"]["minute"]
        targetDayString = event["weekday"]
        timezone = event["timezone"]
    
        # Get the current time in UTC.
        utc_now = pytz.utc.localize(datetime.datetime.now())

        # Calculate the start and end times of the next event.
        dayOfWeek = datetime.datetime.now(pytz.timezone(timezone)).weekday()

        
        targetDay = 7
        if targetDayString == "Monday": targetDay = 0
        elif targetDayString == "Tuesday": targetDay = 1
        elif targetDayString == "Wednesday": targetDay = 2
        elif targetDayString == "Thursday": targetDay = 3
        elif targetDayString == "Friday": targetDay = 4
        elif targetDayString == "Saturday": targetDay = 5
        elif targetDayString == "Sundat": targetDay = 6

        daysUntilTargetDay = (targetDay - dayOfWeek + 7) % 7
        nextWeekday = datetime.timedelta(days=daysUntilTargetDay) + datetime.datetime.now(pytz.timezone(timezone))
        nextWeekday = nextWeekday.replace(hour=eventStartTimeHours, minute=eventStartTimeMinutes, second=0)
        #TODO CONVERT ALL ABOVE INTO GENERIC BASED ON DAT OF THE WEEK SPECIFIED IN BOTCONFIG INSTEAD OF ALWAYS MONDAY

        next_event_start = nextWeekday
        next_event_end = next_event_start + datetime.timedelta(hours=1)

        event_to_create = sched(
            name=event_name,
            description=event_description,
            start_time=next_event_start,
            end_time=next_event_end,
            entity_type=discord.EntityType.external,
            location= "",
            privacy_level= discord.PrivacyLevel.guild_only
        )

        await guild.create_scheduled_event(**event_to_create.getObject())

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

async def eventTask(userSubmitted=False):
    guild = bot.get_guild(bot.guildId)
    eventList = bot.data["eventList"]

    if not userSubmitted:
        for event in eventList:
            eventExists = await checkEventExists(guild, event)
            if eventExists:
                logger.info(f"Event Name: {event['name']} already exists")
                continue
            
            await createEvent(guild, event)