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
        """ Called when a message is sent 
        
        May be not necessary (?)
        """

        if message.author != self.bot.user:
            # await message.channel.send("This is from quote")
            pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """ Called when a message is edited 
        
        May not be necessary (?)
        """

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
        """ Called when a message has a reaction added to it 
        
        When a user reacts to a quote embedded by the bot with the proper reactions,
        it can be sent to him by using DM or it can be saved to their list of personal quotes, 
        it all depends on the reaction used. 
        """
        # await reaction.channel.send("This is from quote")
        pass

    @commands.Cog.listener()
    async def on_private_channel_delete(self, channel):
        """ Called whenever a private channel is deleted 
        
        If a private channel is deleted that had any configuration related to the quote 
        functionality, make sure to also remove it. 
        """
        pass

    @commands.Cog.listener()
    async def on_private_channel_update(self, before, after):
        """ Called whenever a private group DM is updated. e.g. changed name or topic 
        
        Ifa private channel is updated that had any configuration related to the quote
        functionality, make sure to also update it with the newest channel values. 
        """
        pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """ Callend when a Member leaves a Guild 
        
        If the member that left the Guild had any quotes saved, also delete them from the database. 
        """
        pass

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """ Called when a Member updates their profile
        
        This is called when one or more of the following things change:
        - status
        - activity
        - nickname
        - roles

        If the member updates their values, make sure to also update that information
        in the database.       
        """
        pass

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        """ Called when a User updates their profile 
        
        This is called when one or more of the following things change:
        - avatar 
        - username
        - discriminator

        If the user user updates its information, make sure to also update that information
        in the database (?)
        """
        pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """ Callend when a Guild is removed from the Client 
        
        If the Guild is removed, make sure to also remove any stored data.
        """
        pass

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        """ Called when a Guild updates 
        
        If the Guild is updated, make sure to also update the database with the newer values
        """
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

    # Tasks
    @tasks.loop(seconds=10.0)
    async def printer(self):
        logger.warning("This is a warning from quote_cog")

    # Commands
    @commands.group(name="quote", aliases=["qt"], help="Commands for quote generation.")
    async def quote(self, ctx):
        """Commands for quote generation. Use `~help quote` to view subcommands."""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"Incorrect usage. Use {ctx.prefix}help quote for help.")
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

    @quote.command(
        name="list",
        aliases=["ls"],
        brief="Sends list of all categories and authors available.",
        help="Sends list of all categories and authors available.",
    )
    async def quote_list(self, ctx):
        await ctx.send("These are all the categories and authors available.")

    @quote.command(
        name="generate",
        aliases=["gen"],
        brief="Embeds message with a quote in the text channel.",
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
        brief="Programs a quote of the day for the specified channels.",
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
        brief="Displays author and category of a given quote if it finds a match.",
        help="Displays author and category of a given quote if it finds a match.",
    )
    async def quote_detect(self, ctx, *, text=None):
        if text != None:
            await ctx.send("Author and category found for the quote [text].")
        else:
            await ctx.send("Couldn't find author and category for the quote [text].")

    @quote.command(
        name="status",
        brief="Shows the status of the server or channels specified.",
        help="Shows the status of the server or channels specified.",
    )
    async def quote_status(self, ctx, *, channels=discord.TextChannel):
        if channels != None:
            await ctx.send("Status for [server/channel]")
        else:
            await ctx.send("Couldn't get status for [server/channel]")

    # Command Error Handling
    @quote_list.error
    async def quote_list_error(self, ctx, error):
        pass

    @quote_generate.error
    async def quote_generate_error(self, ctx, error):
        pass

    @quote_qotd.error
    async def quote_qotd_error(self, ctx, error):
        pass

    @quote_detect.error
    async def quote_detect_error(self, ctx, error):
        pass

    @quote_status.error
    async def quote_status_error(self, ctx, error):
        pass


def setup(bot):
    bot.add_cog(Quote(bot))
