# Standard library imports
import os
from os.path import dirname, abspath, join
import random
import logging

# Third party imports
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Generate paths
ENVIRONMENT = "local"
BASE_PROJECT_PATH = dirname(dirname(dirname((abspath(__file__)))))
ENV_PATH = join(BASE_PROJECT_PATH, ".envs", f".{ENVIRONMENT}", ".application")
LOGS_PATH = join(BASE_PROJECT_PATH, "data", "output", "logs")
COGS_PATH = join(BASE_PROJECT_PATH, "src", "bot", "cogs")

# Loads environmental variables
load_dotenv(ENV_PATH)
TOKEN = os.getenv("DISCORD_TOKEN")

# Logger configuration

# Create custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
file_name = join(LOGS_PATH, "discord.log")
file_handler = logging.FileHandler(filename=file_name, encoding="utf-8", mode="a")
console_handler = logging.StreamHandler()

# Create formatter and add it to handler
formatter = logging.Formatter(
    "[{asctime}] [{levelname}] {name}: {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Testing logger
logger.warning("This is a warning")
logger.info("This is an info")

# Bot configuration
bot_description = """
    Looking for answers? Knowledge Bot is here to the rescue!

    Check quotes, definitions and translations with very simple commands.
    """
bot_prefix = "="
bot = commands.Bot(command_prefix=bot_prefix, description=bot_description)

# Remove default help command
# bot.remove_command("help")

""" Bot events """


@bot.event
async def on_ready():
    """Called when the bot is ready. """

    # Set bot activity
    activity = discord.Activity(
        name=f"{bot_prefix}help", type=discord.ActivityType.listening,
    )
    await bot.change_presence(activity=activity)

    print(f"Logged in as '{bot.user.name}' (id: {bot.user.id})\n")


@bot.event
async def on_guild_join(guild):
    """ Called when joining a new server.

    Add server to the database (?)

    """
    # Find the first text channel available

    # If general channels exists, create message
    greeting_message = """
    Hi there!, I'm Knowledge Bot, the bot that knows it all (almost). Thanks for adding me to your server.\n

    To get started, use `=help` to check more information about me.\n

    If you need help or find any error, join my support server at https://xyz.com
    """

    # Embed message into general channel
    pass


@bot.event
async def on_guild_remove(guild):
    """ Called when leaving or kicked from a discord server.

    Remove server from the database (?)

    """
    pass


""" Bot commands """


@bot.command
@bot.command(name="load", help="Loads a specified extension/cog")
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")


@bot.command(name="unload", help="Unloads a specified extension/cog")
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")


for filename in os.listdir(COGS_PATH):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


if __name__ == "__main__":
    # Enable bot with Bot application token
    bot.run(TOKEN)
