import discord
from discord.ext import commands, tasks
from discord.utils import get
from resources.models import ScheduleMessageRequest as sched
import asyncio
from datetime import datetime, timedelta
import logging
from typing import List
import pytz

logger = logging.getLogger('discord')

async def sendMessage(bot, request: sched):
    #takes a scheduleMessageRequest and sends it
    channelId = request.getChannelId()
    channel = bot.get_channel(channelId)
    msg = request.getMessage()
    await channel.send(msg)

@tasks.loop(hours=24)
async def scheduleMessages(bot):
    #When the bot starts or json updates shedule all messages written and sent with sendMessage
    async def timer(request, timeDelta):
        await asyncio.sleep(timeDelta)
        await sendMessage(bot, request)

    requests: List[sched] = []
    for msg in bot.data["scheduledMessageList"]:
        requests.append(sched(msg))

    for request in requests:
        timezone = pytz.timezone(request.getTimezone())
        now = datetime.now(timezone)
        target = now.replace(hour=request.getHour(), minute=request.getMinute(), second=0)
        if now > target: target+=timedelta(days=1)
        timeDelta = target - now
        logger.info(f"Target Time: {target} timeDelta: {timeDelta.seconds}")

        asyncio.create_task(timer(request, timeDelta.seconds))



def setup(bot): scheduleMessages.start(bot)