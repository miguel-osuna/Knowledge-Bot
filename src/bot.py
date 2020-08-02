# Standard library imports
import os
import random
import datetime

# Third party imports
import discord
from discord.ext import commands

# Local applications
from config import COGS_PATH, TOKEN
from util.logger import generate_logger

# Logger configuration
logger = generate_logger(__name__)


def _prefix_callable(bot, message):
    """ A callable Prefix for Knowledge Bot. """

    # Check if message  doesn't come from a server
    if not message.guild:
        # Only allow ~ to be used in DMs
        return "~"

    # Retrieve server prefix from the database
    server_prefix = "~"

    # Allow the users to mention the bot or use the server_prefix while being on it.
    return commands.when_mentioned_or(server_prefix)(bot, message)


bot_description = "Looking for answers? Knowledge Bot is here to the rescue!\nCheck quotes, definitions and translations with very simple commands."


class KnowledgeBot(commands.Bot):
    def __init__(self, cogs_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cogs_path = cogs_path

        # Load extensions when initialising the bot
        self.load_extensions()

    def load_extensions(self):
        for filename in os.listdir(self.cogs_path):
            if filename.endswith("py"):
                extension = filename[:-3]
                try:
                    self.load_extension(f"cogs.{extension}")
                except Exception as e:
                    logger.error(f"Failed to load extension {extension} - {e}")

    # Bot Event Listeners
    async def on_ready(self):
        """Called when the client is done preparing the data received from Discord. """

        if not hasattr(self, "uptime"):
            self.uptime = datetime.datetime.utcnow()

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

    async def on_command_error(self, ctx, error):
        """ Called when an error is raised inside a command.

        An error handler that is called when an error is raised inside a command
        either through user input error, check failure, or an error in your own code.
        """

        # This prevent any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, "on_error"):
            return

        # This prEvent Listeners any cogs with an overwritten cog_command
        if (
            ctx.cog is not None
            and ctx.cog._get_overridden_method(ctx.cog.cog_command_error) is not None
        ):
            return

        ignored = None

        # Allows us to check for original exceptions raised and set to CommandInvokeError.
        # If nothing is found, we keep the exception passed to on_command_error
        error = getattr(error, "original", error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            pass

        elif isinstance(error, commands.ConversionError):
            logger.debug("Conversion Error")

        elif isinstance(error, commands.MissingRequiredArgument):
            logger.debug("Missing Required Argument")

        elif isinstance(error, commands.ArgumentParsingError):
            logger.debug("Argument Parsing Error")
            ctx.send(error)

        elif isinstance(error, commands.UnexpectedQuoteError):
            logger.debug("Unexpected Quote Error")

        elif isinstance(error, commands.InvalidEndOfQuotedStringError):
            logger.debug("Invalid End of Quoted String Error")

        elif isinstance(error, commands.ExpectedClosingQuoteError):
            logger.debug("Expected Closing Quote Error")

        elif isinstance(error, commands.BadArgument):
            logger.debug("Bad Argument")

        elif isinstance(error, commands.BadUnionArgument):
            logger.debug("Bad Union Argument")

        elif isinstance(error, commands.PrivateMessageOnly):
            logger.debug("Private Message Only")

        elif isinstance(error, commands.NoPrivateMessage):
            logger.debug(f"No Private Message - {ctx.cog}")
            try:
                await ctx.author.send(
                    f"`{ctx.command}` cannot be used in private messages."
                )
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.CheckFailure):
            logger.debug("Check Failure")

        elif isinstance(error, commands.CheckAnyFailure):
            logger.debug("Check Any Failure")

        elif isinstance(error, commands.DisabledCommand):
            logger.debug("Disabled Command")
            ctx.send(f"Sorry, {ctx.command} has been disabled and cannot be used.")

        elif isinstance(error, commands.CommandInvokeError):
            logger.debug("Command Invoke Error")
            original = error.original

            if not isinstance(original, discord.HTTPException):
                logger.debug(f"In {ctx.command.qualified_name}: {original}.")

        elif isinstance(error, commands.TooManyArguments):
            logger.debug("Too Many Arguments")

        elif isinstance(error, commands.UserInputError):
            logger.debug("User Input Error")

        elif isinstance(error, commands.CommandOnCooldown):
            logger.debug("Command On Cooldown")

        elif isinstance(error, commands.MaxConcurrencyReached):
            logger.debug("Max Concurrency Reached")

        elif isinstance(error, commands.NotOwner):
            logger.debug("Not Owner")

        elif isinstance(error, commands.MissingPermissions):
            logger.debug("Missing Permissions")

        elif isinstance(error, commands.BotMissingPermissions):
            logger.debug("Bot Missing Permissions")

        elif isinstance(error, commands.MissingRole):
            logger.debug("Missing Role")

        elif isinstance(error, commands.BotMissingRole):
            logger.debug("Bot Missing Role")

        elif isinstance(error, commands.MissingAnyRole):
            logger.debug("Missing Any Role")

        elif isinstance(error, commands.BotMissingAnyRole):
            logger.debug("Bot Missing Any Role")

        elif isinstance(error, commands.NSFWChannelRequired):
            logger.debug("NSFW Channel Required")

        elif isinstance(error, commands.ExtensionError):
            logger.debug("Extension Error")

        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            logger.debug("Extension Already Loaded")

        elif isinstance(error, commands.ExtensionNotLoaded):
            logger.debug("Extension Not Loaded")

        elif isinstance(error, commands.NoEntryPointError):
            logger.debug("No Entry Point Error")

        elif isinstance(error, commands.ExtensionFailed):
            logger.debug("Extension Failed")

        elif isinstance(error, commands.ExtensionNotFound):
            logger.debug("Extension Not Found")

        else:
            logger.debug(f"Ignoring exception {error} in command {ctx.command}")

    async def on_command(self, ctx):
        """ Called when an command is found and is about to be invoked. 
        
        An event that is called when a command is found and is about to be invoked. 
        This event is called regardless of whether the command itself succeds via error or completes. 
        """
        pass

    async def on_command_completion(self, ctx):
        """ Callend when a command has comleted its invocation. 
        
        An event that is called when a command has completed its invocation. 
        This event is called only if the command succeded, i.e. all checks have passed and the user input
        it correctly. 
        """
        pass


if __name__ == "__main__":
    # Bot configuration
    knowledge_bot = KnowledgeBot(
        cogs_path=COGS_PATH,
        command_prefix=_prefix_callable,
        description=bot_description,
    )

    # Client event loop initialisation
    knowledge_bot.run(TOKEN)
