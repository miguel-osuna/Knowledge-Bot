# Third party imports
from discord.ext import commands, tasks

# Local applications
from util.logger import generate_logger

logger = generate_logger(__name__)


class HelpCog(commands.Cog):
    def __init__(self, bot):
        """ Initialisation for HelpCog instance. """
        self.bot = bot

    # Events
    @commands.Cog.listener()
    async def on_message(self, message):
        """ Called when a message is sent """

        if message.author != self.bot.user:
            # await message.channel.send("This is from help")
            pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """ Called when an error is raised inside a command.

        An error handler that is called when an error is raised inside a command
        either through user input error, check failure, or an error in your own code.
        """
        pass

    @commands.Cog.listener()
    async def on_command(self, ctx):
        """ Called when an command is found and is about to be invoked. 
        
        An event that is called when a command is found and is about to be invoked. 
        This event is called regardless of whether the command itself succeds via error or completes. 
        """
        pass

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        """ Callend when a command has comleted its invocation. 
        
        An event that is called when a command has completed its invocation. 
        This event is called only if the command succeded, i.e. all checks have passed and the user input
        it correctly. 
        """
        pass


def setup(bot):
    """ Sets the help cog for the bot. """
    bot.add_cog(HelpCog(bot))
