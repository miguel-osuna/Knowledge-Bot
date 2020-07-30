# Standard library imports
import os
import random

# Third party imports
import discord
from discord.ext import commands

# Local applications
from config import COGS_PATH, TOKEN
from util.logger import generate_logger

# Logger configuration
logger = generate_logger(__name__)


class KnowledgeBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Bot events
    async def on_ready(self):
        """Called when the client is done preparing the data received from Discord. """

        # Sets bots status and activity
        status = discord.Status.online
        activity = discord.Activity(
            name=f"{bot_prefix}help", type=discord.ActivityType.listening,
        )
        await self.change_presence(status=status, activity=activity, afk=False)

        app_info = await self.application_info()

        print(app_info)
        print(f"Logged in as '{self.user.name}' (id: {self.user.id})\n")

    async def on_guild_join(self, guild):
        """ Called when a Guild is either created by the Client or when the Client joins a guild

        Add server to the database (?)

        """
        # Find the first text channel available

        # If general channels exists, create message
        greeting_message = """
        Hi there!, I'm Knowledge Bot, the bot that knows it all (almost). Thanks for adding me to your server.\n

        To get started, use `~help` to check more information about me.\n

        If you need help or find any error, join my support server at https://xyz.com
        """

        # Embed message into general channel
        pass

    async def on_guild_remove(self, guild):
        """ Called when leaving or kicked from a discord server.

        Remove server from the database (?)

        """
        pass


if __name__ == "__main__":

    # Bot configuration
    bot_description = """
    Looking for answers? Knowledge Bot is here to the rescue!

    Check quotes, definitions and translations with very simple commands.
    """
    bot_prefix = "~"

    knowledge_bot = KnowledgeBot(command_prefix=bot_prefix, description=bot_description)

    # Bot commands
    @knowledge_bot.command(
        name="load", help="Loads a specified extension/cog", hidden=True
    )
    async def load(ctx, extension):
        knowledge_bot.load_extension(f"cogs.{extension}")

    @knowledge_bot.command(
        name="unload", help="Unloads a specified extension/cog", hidden=True
    )
    async def unload(ctx, extension):
        knowledge_bot.unload_extension(f"cogs.{extension}")

    for filename in os.listdir(COGS_PATH):
        if filename.endswith(".py"):
            knowledge_bot.load_extension(f"cogs.{filename[:-3]}")

    knowledge_bot.run(TOKEN)
