# Third party imports
import discord
from discord.ext import commands, tasks

# Local applications
from util.logger import generate_logger

logger = generate_logger(__name__)


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.printer.start()

    # Events
    @commands.Cog.listener()
    async def on_message(self, message):
        """ Called when a message is sent """

        if message.author != self.bot.user:
            # await message.channel.send("This is from settings")
            pass

    # Tasks
    @tasks.loop(seconds=10.0)
    async def printer(self):
        logger.warning("This is a warning from settings_cog")

    # Commands
    @commands.group(name="settings", aliases=["stgs"])
    async def dictionary(self, ctx):
        """Commands for bot server settings. Use `=help settings` to view subcommands."""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"Incorrect usage. Use {ctx.prefix}help settings for help.")
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

    @dictionary.command(
        name="prefix",
        help="Sets the character for bot prefix. The default bot prefix is `=`.",
    )
    async def settings_prefix(self, ctx, prefix=None):
        if prefix != None:
            await ctx.send("Prefix `[prefix]` setup for bot commands.")
        else:
            await ctx.send("Couldn't setup `[prefix]` as the bots command prefix.")


def setup(bot):
    bot.add_cog(Settings(bot))
