from discord.ext import commands
import logging
from resources.models import ActivityRequest, Poll, ScheduleMessageRequest, ScheduleEventRequest

logger = logging.getLogger('discord')

#Flow

#Part 1
# user runs request command
#   .request <suggestion> <Num participants>
@commands.command(name='request', help='use this command to request a game be played or activity be done')
async def request(ctx, request, *options): 
    # Sesshomaru takes note of the users memberid and the request
    #   Sesshomaru stores the request and the user id together in a file(json for now)
    memmberId = ctx.author.id
    userName = ctx.author.display_name
    
    request = ActivityRequest(request, options, memberId=memmberId, userName=userName)
    logger.info(request.getJson())
# Immediately, Sesshomaru will run a poll with the request with the two options being interested or not interested
#   If the number of interested votes meets or exceeds the number of requested participants, all voters are notified immediately and we enter step 2
#   Poll will last for 30 mins or an hour
#   This poll should be confied to the requests channel, a new channel i will make in general
#   Should have an alternative for core requests
#   OP is immediately considered one of the interested votes
# Sesshomaru periodically runs this interest poll
#   OP might be allowed to decide the length of time to let the request be polled on for
#   User can opt in or out of being notified each time their poll runs or any poll runs
#   OP can opt out of being notified
# If enough people indicate interest(user may define number of yes's and maybe even suggested times?) Then it is considered to be a plan. Step 2

#Part 2
#Sesshomaru takes all voters into account
#Sesshomaru sends a message to all yes voters to suggest a time
#These suggested times will be the answers in this next poll
#Once all the times are set(or the alloted wait period elapses) if there is more than one suggestion a poll is made with each suggestion.
#   If there is only one suggestion:
#       that suggestion wins the poll
#   If there are no suggestions
#       the poll is not done and the users will be notified to decide on a time themselves
#   If there is more than one suggestion
#       Sesshomaru sends out a new poll notifying the interested to pick a date and time
#           alternatively OP can decide on a time themselves
#               this will be overriding this poll and just picking a time at op's suggestion
#   Once a winner is decided, Sesshomaru makes an event for the suggestion at the given time
#Sesshomaru marks all the interested pollers as interested on the event
#   Users can unsign themselves up if they want afterwards

def setup(bot):
    bot.add_command(request)
    return