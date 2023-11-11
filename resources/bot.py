import discord
from discord.ext import commands, tasks
from discord.utils import get
import pytz
import json
import datetime
import os
from models import ScheduleEventRequest as sched

script_dir = os.path.dirname(os.path.realpath(__file__))
jsonFile = os.path.join(script_dir, "botConfig.json")

data = {}
with open(jsonFile, "r") as f:
    data = json.load(f)
f.close()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
bot = commands.Bot(intents=intents, command_prefix = '.')

# Define the event name and description.
token = data["token"]
guildId = data["guildId"]
event_name = data["eventList"][0]["name"]
event_description = data["eventList"][0]["description"]
eventStartTimeHours = data["eventList"][0]["startTime"]["hour"]
eventStartTimeMinutes = data["eventList"][0]["startTime"]["minute"]

# Get the current time in UTC.
utc_now = pytz.utc.localize(datetime.datetime.now())

# Calculate the start and end times of the next event.
dayOfWeek = datetime.datetime.now(pytz.timezone("America/New_York")).weekday()
daysUntilMonday = (7 - dayOfWeek) % 7
nextMonday = datetime.timedelta(days=daysUntilMonday) + datetime.datetime.now(pytz.timezone("America/New_York"))
nextMonday = nextMonday.replace(hour=eventStartTimeHours, minute=eventStartTimeMinutes, second=0)

next_event_start = nextMonday
print(f"Start Time: {next_event_start}")
next_event_end = next_event_start + datetime.timedelta(hours=1)
print(f"End Time: {next_event_end}")

guild = None
event = {}

@bot.event
async def createEvent():
    global guild
    global event
    
    event = sched(
        name=event_name,
        description=event_description,
        start_time=next_event_start,
        end_time=next_event_end,
        entity_type=discord.EntiyType.external,
        location= "",
        privacy_level= discord.PrivacyLevel.guild_only
    )
    """event = {
        "name": event_name,
        "description": event_description,
        "start_time": next_event_start,
        "end_time": next_event_end,
        "entity_type": discord.EntityType.external,
        "location": "",
        "privacy_level": discord.PrivacyLevel.guild_only,
    }"""

@bot.event
async def checkEventExists():
    global guild
    global event_name
    events = await guild.fetch_scheduled_events()
    for event in events:
        if event.name == event_name:
            return True
    else:
        return False


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

    global guild
    guild = bot.get_guild(guildId)

    eventExists = await checkEventExists()
    if eventExists:
        global event_name
        print(f"Event Name: {event_name} already exists")
        return
    
    await createEvent()
    print("Before scheduled event")
    await guild.create_scheduled_event(**event)
    print("After Scheduled event")

# Start the bot.
def run():
    bot.run(token)