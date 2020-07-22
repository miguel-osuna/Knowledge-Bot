import discord
from discord.ext import commands, tasks
import logging

logger = logging.getLogger(__name__)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Events
    @commands.Cog.listener()
    async def on_message(self, message):
        """ Called when a message is sent """

        if message.author != self.bot.user:
            await message.channel.send("This is from help")

    # Commands


def setup(bot):
    """ Sets the help cog for the bot. """
    bot.add_cog(Help(bot))
