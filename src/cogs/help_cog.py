# Third party imports
from discord.ext import commands, tasks

# Local applications
from util.logger import generate_logger

logger = generate_logger(__name__)


class HelpCog(commands.Cog, name="Help"):
    def __init__(self, bot):
        """ Initialisation for HelpCog instance. """
        self.bot = bot

    # Event Listeners
    @commands.Cog.listener()
    async def on_message(self, message):
        """ Called when a message is sent """

        if message.author != self.bot.user:
            # await message.channel.send("This is from help")
            pass

        # Class Methods

    # Class methods
    async def cog_command_error(self, ctx, error):
        """ A special method that is called whenever an error is dispatched inside this cog. 
        
        This is similar to on_command_error() except only applying to the commands inside this cog.
        """

        ignored = None

        if isinstance(error, ignored):
            return

        else:
            return

    async def cog_before_invoke(self, ctx):
        """ A special method that acts as a cog local pre-invoke hook. """
        await ctx.trigger_typing()
        return await super().cog_before_invoke(ctx)

    async def cog_after_invoke(self, ctx):
        """ A special method that acts as a cog local post-invoek hook. """
        return await super().cog_after_invoke(ctx)


def setup(bot):
    """ Sets up the help cog for the bot. """
    logger.info("Loading Help Cog")
    bot.add_cog(HelpCog(bot))


def teardown(bot):
    """ Tears down the help cog for the bot. """
    logger.info("Unloading Help Cog")
    bot.remove_cog("cogs.help_cog")
