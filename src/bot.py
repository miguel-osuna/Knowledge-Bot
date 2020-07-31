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
            name=f"{self.command_prefix}help", type=discord.ActivityType.listening,
        )
        await self.change_presence(status=status, activity=activity, afk=False)

        print(
            f"\nLogged in as '{self.user.name}' - (id: {self.user.id})\nVersion: {discord.__version__}\n"
        )

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


def get_prefix(bot, message):
    """ A callable Prefix for Knowledge Bot. """

    # Check if message  doesn't come from a server
    if not message.guild:
        # Only allow ~ to be used in DMs
        return "~"

    # Retrieve server prefix from the database
    server_prefix = "~"

    # Allow the users to mention the bot or use the server_prefix while being on it.
    return commands.when_mentioned_or(server_prefix)(bot, message)


if __name__ == "__main__":
    # Bot configuration
    bot_description = "Looking for answers? Knowledge Bot is here to the rescue!\nCheck quotes, definitions and translations with very simple commands."
    knowledge_bot = KnowledgeBot(command_prefix=get_prefix, description=bot_description)

    for filename in os.listdir(COGS_PATH):
        if filename.endswith("py"):
            extension = filename[:-3]
            try:
                knowledge_bot.load_extension(f"cogs.{extension}")
            except Exception as e:
                logger.error(f"Failed to load extension {extension}")

    # Client event loop initialisation
    knowledge_bot.run(TOKEN, bot=True, reconnect=True)
