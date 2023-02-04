"""
Cog. Defines base commands and listeners used by the bot.
Setup acts as entry point to add cog to bot.
"""

import logging
import os

from discord.ext import commands

log = logging.getLogger(__name__)

class Base(commands.Cog):
    """Basic commands and listeners"""

    def __init__(self, bot):
        self.bot = bot
        # self.channel = channel
        self.ready_state = False

    @commands.Cog.listener()
    async def on_ready(self):
        """Send message when bot comes online"""

        if not self.ready_state:
            log.info("InsultBot Online")

            if os.environ['SYNC_TREE'] == "true":
                log.info("Syncing command tree...")
                await self.bot.tree.sync()
                log.info("Done.")

            self.ready_state = True

async def setup(bot):
    await bot.add_cog(Base(bot))
