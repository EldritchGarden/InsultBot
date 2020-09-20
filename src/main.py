"""
Main program execution flow entry point. Imports Cogs
and creats a bot object with the cogs added. Finally
starts the bot.
"""

import json
import logging
import sys
import os
import time

from discord.ext import commands

from CogLib import base, admin, insult

# Pre-Initialization #
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # ensure correct dir

with open('config.json', 'r') as conf_file:
    config = json.load(conf_file)

# configure logging
log_file = time.strftime("%m%d%y-%H%M") + '.log'

sout_fmt = logging.Formatter("%(module)s - %(levelname)s :: %(message)s")
file_fmt = logging.Formatter(
    "(%(asctime)s) %(module)s [%(funcName)s] - %(levelname)s :: %(message)s")

sout_handle = logging.StreamHandler(stream=sys.stdout)
sout_handle.setFormatter(sout_fmt)
sout_handle.setLevel(config['log_level'])

file_handle = logging.FileHandler(log_file)
file_handle.setFormatter(file_fmt)
file_handle.setLevel(config['log_level'])

logging.basicConfig(handlers=(sout_handle, file_handle), datefmt="%m%d-%H:%M.%S",
                    level=config['log_level'])

log = logging.getLogger(__name__)  # create logger
log.info("Logging initialized")

# Initialize bot #
log.debug("Importing Cogs...")

log.info("Bot prefix set as %s" % config['prefix'])
bot = commands.Bot(config['prefix'])

log.debug("Setting up Cogs...")
base.setup(bot, config['default_channel'])
admin.setup(bot, config['default_channel'], config['administrators'])
insult.setup(bot)

log.info("Starting bot...")
bot.run(config['token'])
