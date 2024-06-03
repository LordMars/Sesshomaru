import discord
from discord.ext import commands, tasks
from discord.utils import get
from handlers import tasks, scheduledMessages, delaneyJail
import logging
import json
import os
import asyncio

from handlers.deprecated import events, poll

logger = logging.getLogger('discord')

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix = '.')

@bot.event
async def on_ready():
    logger.info(f"We have logged in as {bot.user}")
    poll.setup(bot)
    scheduledMessages.setup(bot)
    delaneyJail.setup(bot)
    tasks.setup(bot)

# Start the bot.
def run():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    jsonFile = os.path.join(script_dir+"/resources", "botConfig.json")

    with open(jsonFile, "r") as f:
        data = json.load(f)

        # Define the event name and description.
        token = data["token"]
        delaneyJail.setToken(token)

        bot.guildId = data["guildId"]
        bot.data = data

        bot.run(token)
    f.close()