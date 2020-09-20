"""
Cog. Defines commands and functions for creating insults.
Commands return the insult, local functions are used to read
and generate the insults.

Setup is entry point for the cog.
"""

# Standard Library
import random
from pathlib import Path
import logging
import re

# External
from discord.ext import commands
import inflect


log = logging.getLogger(__name__)
p = inflect.engine()


class Insult(commands.Cog):
    """Defines methods for reading wordlists, generating insults,
    and defines commands for insult and insultsfw
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['insultsfw'])
    async def insult(self, ctx, *args):
        """Generate and send an insult.
        """

        # If insult bot is mentioned, send middle finger and return
        if re.search("<@!?548617277000384532", ctx.message.content):
            await ctx.send("\U0001F595")  # send :middle_finger:
            return

        if ctx.invoked_with == 'insultsfw':
            insult = self._make_insult(args, sfw=True)
        else:
            insult = self._make_insult(args)

        await ctx.message.delete()  # delete original message
        await ctx.send(insult)

    def _make_insult(self, args, sfw=False):
        """Generate an insult with context

        Args:
            ctx (Context): Discord invocation context
            sfw (bool) [optional]: if true generate a safe for work insult

        Returns:
            string: content of generated insult, formatted
        """

        words = self._read_word_lists()

        if sfw:
            insult = "{adjective} {curse} {noun}".format(
                adjective=random.choice(words[0]),
                curse=random.choice(words[0]),  # use adjective instead of curse
                noun=random.choice(words[2])
            )
        else:
            insult = "{adjective} {curse} {noun}".format(
                adjective=random.choice(words[0]),
                curse=random.choice(words[1]),
                noun=random.choice(words[2])
            )

        if not args:
            content = "You " + insult
        else:
            if p.singular_noun(args[-1]):  # plural
                # make insult plural
                insult = insult.split()
                insult[2] = p.plural_noun(insult[2])
                content = ' '.join(args) + " are " + ' '.join(insult)
            else:  # singular
                content = ' '.join(args) + ' is ' + p.a(insult)

        return content

    def _read_word_lists(self):
        """Read word lists and parse into lists

        Returns:
            tuple: [0] adjectives, [1] curses, [2] nouns
        """

        with open(str(Path('Wordlists') / 'adjectives.csv'), 'r') as file:
            adjectives = file.read().splitlines()

        with open(str(Path('Wordlists') / 'nouns.csv'), 'r') as file:
            nouns = file.read().splitlines()

        with open(str(Path('Wordlists') / 'curses.csv'), 'r') as file:
            curses = file.read().splitlines()

        return (adjectives, curses, nouns)


def setup(bot):
    """Add cog to bot. Called in main.
    """

    bot.add_cog(Insult(bot))
