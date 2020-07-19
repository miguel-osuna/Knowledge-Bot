# Standard library imports
from os import getenv
from os.path import dirname, abspath, join
import random

# Third party imports
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Generate paths
ENVIRONMENT = "local"
BASE_PROJECT_PATH = dirname(dirname(dirname((abspath(__file__)))))
ENV_PATH = join(BASE_PROJECT_PATH, ".envs", f".{ENVIRONMENT}", ".application")
LOGS_PATH = join(BASE_PROJECT_PATH, "data", "output", "logs")

# Loads environmental variables
load_dotenv(ENV_PATH)
TOKEN = getenv("DISCORD_TOKEN")
GUILD = getenv("DISCORD_GUILD")

bot = commands.Bot(command_prefix="!")

# Bot command
@bot.command(name="99", help="Responds with a random quote from Brookly 99")
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        "I'm the human form of the 💯 emoji.",
        "Bingpot!",
        (
            "Cool. Cool cool cool cool cool cool cool, "
            "no doubt no doubt no doubt no doubt."
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


# Bot command checking predicates
# Allow users that have an 'admin' role to create new channels on the discord server
@bot.command(name="create_channel", help="Creates a channel on the server.")
@commands.has_role("admin")
async def create_channel(ctx, channel_name="real-python"):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)

    # Check if there's not an existing channel
    if not existing_channel:
        print(f"Creating channel: {channel_name}")
        await guild.create_text_channel(channel_name)


# Catches command errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")


bot.run(TOKEN)

if __name__ == "__main__":
    pass
