"""
Cog. Defines base commands and listeners used by the bot.
Setup acts as entry point to add cog to bot.
"""

import logging

from discord.ext import commands

log = logging.getLogger(__name__)

INFO = """
Insult your friends with InsultBot! InsultBot creates randomly generated insults
following a particular formula to creatively insult whatever you want.
"""


class Base(commands.Cog):
    """Basic commands and listeners"""

    def __init__(self, bot, channel):
        self.bot = bot
        self.channel = channel
        self.ready_state = False

    @commands.Cog.listener()
    async def on_ready(self):
        """Send message when bot comes online"""

        if not self.ready_state:
            print("InsultBot Online")
            await self.bot.get_channel(self.channel).send("InsultBot online")
            self.ready_state = True

    @commands.command()
    async def info(self, ctx):
        """Displys information"""

        await ctx.send(INFO)


def setup(bot, channel):
    bot.add_cog(Base(bot, channel))
