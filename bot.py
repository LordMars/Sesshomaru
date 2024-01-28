import discord
from discord.ext import commands, tasks
from discord.utils import get
from handlers import poll, scheduledMessages, events
import logging
import json
import os
import asyncio

logger = logging.getLogger('discord')

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix = '.')

@bot.event
async def on_ready():
    logger.info(f"We have logged in as {bot.user}")
    poll.setup(bot)

# Start the bot.
def run():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    jsonFile = os.path.join(script_dir+"/resources", "botConfig.json")

    with open(jsonFile, "r") as f:
        data = json.load(f)

        # Define the event name and description.
        token = data["token"]
        bot.guildId = data["guildId"]
        bot.data = data

        bot.run(token)
    f.close()