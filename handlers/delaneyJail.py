import discord
from discord.ext import commands, tasks
from discord.utils import get
from handlers import tasks
from resources import models
import logging
import requests
import time
import asyncio

logger = logging.getLogger('discord')

curCtx = None
curPoll = None
voteLimit = 3
sleepSeconds = 300
token = ""
delaneyId = 160847743974244352
criminalId = 1246818307131183225
jailTime = 10

@commands.command(name='arrest', help='use this command to arrest delaney and vote on his temporary banishment')
async def arrest(ctx):
    logger.info("UNDER ARREST")
    await poll(ctx)

async def poll(ctx):
    #create a poll
    # after a certain period of time use the poll to determine if a timeout should be don
    global curPoll
    global curCtx
    if curPoll: return 

    curCtx = ctx
    request = models.Poll().getJson()
    url = rf"https://discord.com/api/v10/channels/{ctx.channel.id}/messages"
    curPoll = requests.post(url, json=request, headers={"Authorization":"Bot "+token})
    asyncio.get_event_loop().create_task(pollProgress(ctx))

async def pollProgress(ctx):
    #runs poll for a given amount of time
    #while not curPoll: pass
    global curPoll
    if not curPoll.ok: logger.info(curPoll.reason)
    while not curPoll.json()["poll"]["results"]["is_finalized"]:
        for answer in curPoll.json()["poll"]["results"]["answer_counts"]:
            if answer["id"] == 1:
                if answer["count"] >= voteLimit:
                    url = rf"https://discord.com/api/v10/channels/{ctx.channel.id}/polls/{curPoll.json()['id']}/expire"
                    requests.post(url, headers={"Authorization":"Bot "+token})
                    await verdict(ctx, curPoll.json()["poll"]["results"]["answer_counts"])
                    return
                
        await asyncio.sleep(sleepSeconds)

        url = rf"https://discord.com/api/v10/channels/{ctx.channel.id}/messages/{curPoll.json()['id']}"
        req = requests.get(url, headers={"Authorization":"Bot "+token})
        logger.info(req.json())
        if req.ok:
            curPoll = req
        else:
            logger.info(f"curPoll update grab failure {req.reason}")

    await verdict(ctx, curPoll.json()["poll"]["results"]["answer_counts"])

async def verdict(ctx, answerCounts):
    #Determines if the poll should result in administrative action
    guilty = 0

    yes = 0
    no = 0
    meh = 0
    for answer in answerCounts:
        if answer["id"] == 1:
            yes = answer["count"]
        elif answer["id"] == 2:
            meh = answer["count"]
        else:
            no = answer["count"]
    guilty = yes + meh

    if yes >= no or guilty > no:
        await sentencing(ctx)

    global curPoll
    curPoll = None
    return

async def sentencing(ctx):
    #determines the exact nature of the aadministrative action to take
    #apply role to delaney
    logger.info("sentencing delaney")
    member = ctx.guild.get_member(delaneyId)
    role = discord.utils.get(ctx.guild.roles, id=criminalId)
    await member.add_roles(role)

    asyncio.get_event_loop().create_task(serve(ctx, jailTime))

async def serve(ctx, jailTime):
    #serve the time
    logger.info("delaney serving jailtime")
    await asyncio.sleep(jailTime*60)
    await release(ctx)

async def release(ctx):
    #undo sentencing after its served
    #remove role from delaney
    logger.info("release the delaney")
    member = ctx.guild.get_member(delaneyId)
    role = discord.utils.get(ctx.guild.roles, id=criminalId)
    await member.remove_roles(role)

def setup(bot):
    bot.add_command(arrest)
    return

def setToken(t):
    global token
    token = t