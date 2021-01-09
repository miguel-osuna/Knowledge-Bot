import os
from os.path import dirname, abspath, join
from datetime import datetime

import discord
from discord.ext import commands

from util import generate_logger
from config import (
    SUPPORT_SERVER_INVITE_URL,
    BOT_INVITE_URL,
    DISCORD_TOKEN,
    COMMAND_PREFIX,
    COGS_PATH,
    BASE_PROJECT_PATH,
)

# Logger configuration
logger = generate_logger(__name__)


class KnowledgeBot(commands.Bot):
    def __init__(self, cogs_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cogs_path = cogs_path

        # Load extensions when initialising the bot
        self.load_extensions()

    def load_extensions(self):
        """ Loads the bot cogs. """

        for filename in os.listdir(self.cogs_path):
            if filename.endswith("py"):
                extension = filename[:-3]
                try:
                    self.load_extension(f"cogs.{extension}")
                except Exception as e:
                    logger.error(f"Failed to load extension {extension}\n{e}")

    # Bot Event Listeners
    async def on_ready(self):
        """ Called when the client is done preparing the data received from Discord. """

        if not hasattr(self, "uptime"):
            self.uptime = datetime.utcnow()

        # Sets bots status and activity
        status = discord.Status.online
        activity = discord.Activity(
            name=f"{self.command_prefix}help", type=discord.ActivityType.listening
        )
        await self.change_presence(status=status, activity=activity, afk=False)

        logger.info(
            f"\nLogged in as '{self.user.name}'\n(id: {self.user.id})\nVersion: {discord.__version__}\n"
        )

    async def on_guild_join(self, guild):
        """Called when a Guild is either created by the Client or when the Client joins a guild

        Add server to the database (?)
        """
        # Find the first text channel available

        # If general channels exists, create message
        support_server_invite_url = SUPPORT_SERVER_INVITE_URL

        greeting_message = f"""Hi there, I'm Knowledge Bot, thanks for adding me to your server.\n
                               To get started, use `-help` to check more information about me.\n
                               If you need help or find any error, join my support server at {support_server_invite_url}."""

        greeting_message = """
        Hi there!, I'm Knowledge Bot, the bot that knows it all (almost). Thanks for adding me to your server.\n

        To get started, use `~help` to check more information about me.\n

        If you need help or find any error, join my support server at https://xyz.com
        """

        # Embed message into general channel

    async def on_guild_remove(self, guild):
        """Called when leaving or kicked from a discord server. """

        # Find the first text channel available

        # If general channel exists, create message
        leave_message = f"""Thanks for adding Knowledge Bot to your server.\n
                            If you wish to add it again, use {BOT_INVITE_URL}\n
                            Have a nice day! """


if __name__ == "__main__":
    bot_description = """Looking for answers? Knowledge Bot is here to the rescue!\n
                         Check quotes, definitions and translations with very simple commands."""

    intents = discord.Intents.default()
    intents.members = True

    knowledge_bot = KnowledgeBot(
        cogs_path=COGS_PATH,
        command_prefix=COMMAND_PREFIX,
        description=bot_description,
        intents=intents,
    )

    # Client event loop initialisation
    knowledge_bot.run(DISCORD_TOKEN)
