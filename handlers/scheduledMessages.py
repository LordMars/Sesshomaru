import discord
from discord.ext import commands, tasks
from discord.utils import get
from resources.models import ScheduleMessageRequest as sched
import logging

logger = logging.getLogger('discord')
intents = discord.Intents.default()
bot = commands.Bot(intents=intents, command_prefix = '.')

def sendMessage(): pass
def scheduleMessage(): pass