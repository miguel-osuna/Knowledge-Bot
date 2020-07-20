# Standard library imports
import os
from os.path import dirname, abspath, join
import random

# Third party imports
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Local application imports

# Generate paths
ENVIRONMENT = "local"
BASE_PROJECT_PATH = dirname(dirname(dirname((abspath(__file__)))))
ENV_PATH = join(BASE_PROJECT_PATH, ".envs", f".{ENVIRONMENT}", ".application")
LOGS_PATH = join(BASE_PROJECT_PATH, "data", "output", "logs")
COGS_PATH = join(BASE_PROJECT_PATH, "knowledge_bot", "bot", "cogs")

# Loads environmental variables
load_dotenv(ENV_PATH)
TOKEN = os.getenv("DISCORD_TOKEN")

# Bot configuration
bot_description = """
    Looking for answers? Knowledge Bot is here to the rescue!
    
    Check quotes, definitions and translations with very simple commands. 
    """
bot_prefix = "="
bot = commands.Bot(command_prefix=bot_prefix, description=bot_description)

""" Bot events """

# When bot is ready
@bot.event
async def on_ready():

    # Set bot activity
    activity = discord.Activity(
        name=f"Write {bot_prefix}help for more info.",
        type=discord.ActivityType.listening,
    )
    await bot.change_presence(activity=activity)

    print(f"Logged in as '{bot.user.name}' (id: {bot.user.id})\n")


""" Bot commands """


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
