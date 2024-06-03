import discord
from discord.ext import commands, tasks
from discord.utils import get
import logging

logger = logging.getLogger('discord')

@commands.command(name='poll', help='Create a poll. Usage: /poll "Question" "Option 1" "Option 2" ...')
async def poll(ctx, question, *options):
    logger.info("Poll command called")
    try:
        # Check if at least two options are provided
        if len(options) < 2:
            await ctx.send('Please provide at least two options for the poll.')
            return

        # Create an embed for the poll
        embed = discord.Embed(title=question, color=discord.Color.blue())

        # Add options to the embed
        for i, option in enumerate(options, start=1):
            reaction = f'\U0001F1E6'
            embed.add_field(name=chr(ord(reaction) + i - 1), value=option, inline=True)

        # Send the poll message
        poll_message = await ctx.send(embed=embed)

        # Add reactions to the poll message for each option
        for i in range(len(options)):
            reaction = f'\U0001F1E6'  # Regional Indicator Symbol Letter A (🇦)
            reaction = chr(ord(reaction) + i)  # Increment the Unicode code point
            await poll_message.add_reaction(reaction)
    except commands.errors.InvalidEndOfQuotedStringError:
        await ctx.send("Please add spaces between all options enclosed in quotes.")
        pass
    except commands.errors.ExpectedClosingQuoteError:
        await ctx.send("Please close all quotes.")
        pass
    except commands.errors.MissingRequiredArgument:
        await ctx.send("Please provide a question and atleast two options.")
        pass

    def timeLimit():
        #Check if the user submitted a time limit for the poll to close
        pass

    def showResult():
        #once a polls elapsed time has passed end the poll and show the final result
        pass

def setup(bot):
    logger.info("Poll Setup")
    bot.add_command(poll)