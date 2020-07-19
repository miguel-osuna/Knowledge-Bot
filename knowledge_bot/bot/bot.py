# Standard library imports
from os import getenv
from os.path import dirname, abspath, join
import random

# Third party imports
import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv

# Local application imports\

# Generate paths
ENVIRONMENT = "local"
BASE_PROJECT_PATH = dirname(dirname(dirname((abspath(__file__)))))
ENV_PATH = join(BASE_PROJECT_PATH, ".envs", f".{ENVIRONMENT}", ".application")
LOGS_PATH = join(BASE_PROJECT_PATH, "data", "output", "logs")

# Loads environmental variables
load_dotenv(ENV_PATH)
TOKEN = getenv("DISCORD_TOKEN")

bot_description = "Looking for answers? Knowledge Bot is here to the rescue!"
bot = Bot(command_prefix="=", description=bot_description)

# Bot events
@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("----------")


# Quote commands
@bot.command(name="quote", help="Generate a quote.")
async def generate_quote(
    ctx, category=None, author=None, type="random", language="english"
):
    await ctx.send("You know nothing, John Snow")


# Translate commands
channel_default_language = "english"


@bot.command(name="translate", help="Translate a word or phrase.")
async def translate_text(
    ctx, from_language=channel_default_language, to_language=None, text=None
):

    if to_language != None:
        await ctx.send("Text translated.")

    else:
        await ctx.send("Couldn't translate language.")


# Definition commands
@bot.command(name="definition", help="Looks for the definition of a word")
async def text_definition(
    ctx, word: str, word_language="english", definition_language="english"
):
    if word:
        await ctx.send("This is your definition.")


# Settings commands
@bot.command(name="settings", help="Configure Knowledge Bot in your server")
async def bot_settings(ctx, command, prefix, value):
    await ctx.send("Your settings have changed.")


if __name__ == "__main__":
    # Enable bot with Bot application token
    bot.run(TOKEN)
