# Third party imports
import discord
from discord.ext import commands, tasks

# Local applications
from util.logger import generate_logger

logger = generate_logger(__name__)


class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.printer.start()

    # Events
    @commands.Cog.listener()
    async def on_message(self, message):
        """ Called when a message is sent """

        if message.author != self.bot.user:
            # await message.channel.send("This is from quote")
            pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """ Called when a message is edited """

        prev_message = before
        next_message = after

        if (
            prev_message.author != self.bot.user
            and next_message.author != self.bot.user
        ):
            # await next_message.channel.send("This is from quote")
            pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """ Called when a message has a reaction added to it """
        # await reaction.channel.send("This is from quote")
        pass

    @commands.Cog.listener()
    async def on_private_channel_delete(self, channel):
        """ Called whenever a private channel is deleted """
        pass

    @commands.Cog.listener()
    async def on_private_channel_update(self, before, after):
        """ Called whenever a private group DM is updated. e.g. changed name or topic """
        pass

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """ Called when a Member updates their profile """
        pass

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        """ Called when a User updates their profile """
        pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """ Callend when a Guildis removed from the Client """
        pass

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        """ Called when a Guild updates """
        pass

    # Tasks
    @tasks.loop(seconds=10.0)
    async def printer(self):
        logger.warning("This is a warning from quote_cog")

    # Commands
    @commands.group(name="quote", aliases=["qt"])
    async def quote(self, ctx):
        """Commands for quote generation. Use `=help quote` to view subcommands."""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"Incorrect usage. Use {ctx.prefix}help quote for help.")
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

    @quote.command(
        name="list",
        aliases=["ls"],
        help="Sends a list of all categories and authors available.",
    )
    async def quote_list(self, ctx):
        await ctx.send("These are all the categories and authors available.")

    @quote.command(
        name="generate",
        aliases=["gen"],
        help="Embeds message with a quote in the text channel. If no parameter is specified, it displays a random quote.",
    )
    async def quote_generate(
        self, ctx, category=None, author=None, type="random", language="english"
    ):
        if category != None and author != None:
            await ctx.send("Quote generated.")
        else:
            await ctx.send("Couldn't generate quote.")

    @quote.command(
        name="qotd",
        help="Programs a quote of the day for the specified channels. The default language for the quote is english.",
    )
    async def quote_qotd(
        self,
        ctx,
        status=None,
        category=None,
        author=None,
        time=None,
        language="english",
        *,
        channels=discord.TextChannel,
    ):
        if (
            status != None
            and category != None
            and author != None
            and time != None
            and channels != None
        ):
            await ctx.send(
                "Quote programmed daily at [time] for channels #[channel] and #[channel]"
            )
        else:
            await ctx.send(
                "Couldn't program daily quote for channels #[channel] and #[channel]"
            )

    @quote.command(
        name="detect",
        help="Displays author and category of the quote if it finds a match.",
    )
    async def quote_detect(self, ctx, *, text=None):
        if text != None:
            await ctx.send("Author and category found for the quote [text].")
        else:
            await ctx.send("Couldn't find author and category for the quote [text].")

    @quote.command(
        name="status", help="Shows the status of the server or channels specified."
    )
    async def quote_status(self, ctx, *, channels=discord.TextChannel):
        if channels != None:
            await ctx.send("Status for [server/channel]")
        else:
            await ctx.send("Couldn't get status for [server/channel]")


def setup(bot):
    bot.add_cog(Quote(bot))
