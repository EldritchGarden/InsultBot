"""
Main program execution flow entry point. Imports Cogs
and creats a bot object with the cogs added. Finally
starts the bot.
"""

import logging
import sys
import os
import time
from asyncio import run

from discord.ext import commands
from discord import Intents

from CogLib import base, insult
import update

# Pre-Initialization #
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # ensure correct dir

# configure logging
log_file = time.strftime("%m%d%y-%H%M") + '.log'
log_level = int(os.environ['LOG_LEVEL'])

sout_fmt = logging.Formatter("%(module)s - %(levelname)s :: %(message)s")
file_fmt = logging.Formatter(
    "(%(asctime)s) %(module)s [%(funcName)s] - %(levelname)s :: %(message)s")

sout_handle = logging.StreamHandler(stream=sys.stdout)
sout_handle.setFormatter(sout_fmt)
sout_handle.setLevel(log_level)

file_handle = logging.FileHandler(log_file)
file_handle.setFormatter(file_fmt)
file_handle.setLevel(log_level)

logging.basicConfig(handlers=(sout_handle, file_handle), datefmt="%m%d-%H:%M.%S",
                    level=log_level)

log = logging.getLogger(__name__)  # create logger
log.info("Logging initialized")

if not os.environ['BOT_TOKEN']:
    log.error("Bot token not set! Set a bot token with '-e BOT_TOKEN='<token>''")
    raise SystemExit("No Bot Token Set")

log.info("Fetching word lists...")
update.wordlists(os.environ['GIST'], ['adjectives.csv', 'curses.csv', 'nouns.csv'])

# Initialize bot #
log.debug("Importing Cogs...")

log.info(f"Bot prefix set as {os.environ['BOT_PREFIX']}")
bot = commands.Bot(os.environ['BOT_PREFIX'], intents=Intents.default())

async def register_cogs():
    log.debug("Setting up Cogs...")
    await base.setup(bot)
    await insult.setup(bot)

run(register_cogs())

log.info("Starting bot...")
bot.run(os.environ['BOT_TOKEN'])
