"""
Cog. Defines commands relating to admin activities.
Class Admin subclasses commands.Cog from discord py.
Commands are defined using the @commands.command()
decorator. Commands should almost always be asnyc.

The setup function is the entry point the bot uses
to add the Cog.
"""

import logging

from discord.ext import commands

from Updater import update
from admin_check import check_admin


log = logging.getLogger(__name__)


class Admin(commands.Cog):
    """Collection of commands requiring admin access"""

    def __init__(self, bot, channel, admins):
        self.bot = bot
        self.channel = channel
        self.admins = admins

    @commands.command(hidden=True)
    async def get_channel_id(self, ctx):
        """Get channel id where command was run"""

        if check_admin(ctx.author.id):
            await self.bot.get_channel(self.admins).send(
                'Channel ID: {}'.format(ctx.channel.id)
            )
        else:
            await ctx.send("Only admins can perform this action")

    @commands.command(hidden=True)
    async def get_user_id(self, ctx, *arg):
        """Gets the user id of the user mentioned.
        Format: $get_user_id @user"""

        if check_admin(ctx.author.id):
            try:
                user_id = arg[0].replace('<', '').replace('>', '')
            except ValueError as err:
                await ctx.send("Invalid command format")
                log.error(arg[0])
                log.error(err)
                return

            await self.bot.get_channel(self.channel).send(user_id)
        else:
            await ctx.send("Only admins can perform this action")

    @commands.command()
    async def update(self, ctx):
        """Attempts to update local wordlists automatically"""

        try:
            update.main()
        except Exception as error:
            await ctx.send("An error was encountered while updating")
            log.error(error)
            return

        await ctx.send("Word lists successfully updated")

    @commands.command()
    async def shutdown(self, ctx):
        """Force raise a SystemExit to shut down bot"""

        if check_admin(ctx.author.id):
            await ctx.send("Shutting Down")
            log.warning("Shutdown command triggered, raising SystemExit")
            raise SystemExit
        else:
            await ctx.send("Only admins can perform this action")


def setup(bot, channel, admins):
    """Setup routine on bot start"""

    bot.add_cog(Admin(bot, channel, admins))
