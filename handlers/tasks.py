import discord
from discord.ext import commands, tasks
from discord.utils import get
import logging

logger = logging.getLogger('discord')

@commands.command(name='addtask', help='Add a task to Sesshomarus dev list. Usage:.addtask "[task]"')
async def addtask(ctx, task):
    pass

async def viewtasks(ctx):
    pass

def setup(bot):
    bot.add_command(addtask)
    #bot.add_command(viewtasks)
    pass