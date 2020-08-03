# Third party imports
import discord
from discord.ext import commands, tasks

# Local applications
from util.logger import generate_logger

logger = generate_logger(__name__)


class Prefix(commands.Converter):
    """ Prefix argument converter for user input. """

    async def convert(self, ctx, argument):
        user_id = ctx.bot.user.id
        if argument.startswith((f"<@{user_id}>", f"<@!{user_id}>")):
            raise commands.BadArgument("That is a reserver prefix already in use.")
        return argument


class SettingsCog(commands.Cog, name="Settings"):
    def __init__(self, bot):
        """ Initialisation for SettingsCog instance. """
        self.bot = bot
        self.printer.start()

    # Event Listeners
    @commands.Cog.listener()
    async def on_message(self, message):
        """ Called when a message is sent 
        
        May not be needed (?)
        """

        if message.author != self.bot.user:
            # await message.channel.send("This is from settings")
            pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """ Called when a message is edited 
        
        May not be needed (?)
        """

        prev_message = before
        next_message = after

        if (
            prev_message.author != self.bot.user
            and next_message.author != self.bot.user
        ):
            # await next_message.channel.send("This is from settings")
            pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """ Called when a message has a reaction added to it 
        
        May not be needed (?)
        """
        # await reaction.channel.send("This is from settings")
        pass

    @commands.Cog.listener()
    async def on_private_channel_delete(self, channel):
        """ Called whenever a private channel is deleted 
        
        May not be needed (?)
        """
        pass

    @commands.Cog.listener()
    async def on_private_channel_update(self, before, after):
        """ Called whenever a private group DM is updated. e.g. changed name or topic 
        
        May not be needed (?)
        """
        pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """ Callend when a Member leaves a Guild 
        
        May not be needed (?)
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
        
        May not be needed (?)
        """
        pass

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        """ Called when a User updates their profile

        This is called when one or more of the following things change:
        - avatar 
        - username
        - discriminator
        
        May not be needed (?)
        """
        pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """ Callend when a Guild is removed from the Client 
        
        If the Guild that was removed from the Client had any configuration related 
        to the settings functionality, make sure to also remove any data from the database
        """
        pass

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        """ Called when a Guild updates 
        
        When a Guild updates its information, also make sure this new values to update
        the database
        """
        pass

    # Class Methods
    async def cog_before_invoke(self, ctx):
        """ A special method that acts as a cog local pre-invoke hook. """
        await ctx.trigger_typing()
        return await super().cog_before_invoke(ctx)

    async def cog_after_invoke(self, ctx):
        """ A special method that acts as a cog local post-invoek hook. """
        return await super().cog_after_invoke(ctx)

    # Tasks
    @tasks.loop(seconds=10.0)
    async def printer(self):
        # logger.warning("This is a warning from settings_cog")
        pass

    # Commands
    @commands.group(
        name="settings", aliases=["stgs"], help="Commands for bot server settings."
    )
    async def settings(self, ctx):
        """Commands for bot server settings. Use `~help settings` to view subcommands."""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"Incorrect usage. Use {ctx.prefix}help settings for help.")
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

    @commands.group(
        name="prefix",
        aliases=["prfx"],
        help="Manages the servers's custom prefixes.",
        invoke_without_command=True,
    )
    async def prefix(self, ctx):
        """ Manages the server's custom prefixes. 
        
        If called without a subcommand, this will list the currently set
        prefixes
        """
        pass

    @prefix.command(
        name="add",
        help="Appends a prefix to the list of custom prefixes",
        ignore_extra=False,
    )
    async def prefix_add(self, ctx, prefix: Prefix):
        """ Appends a prefix to the list of custom prefixes. 

        To have a word prefix, you should quote it and end it with a space, e.g.
        "hello" to set the prefix to "hello'. This is because Discord removes
        spaces when sending messages so the spaces are not preserved. 

        Multi-word prefixes must be quoted also.

        You must have manage server permission to use this command.
        """
        pass

    @prefix.command(
        name="remove",
        help="Removes a prefix from the list of custom prefixes.",
        ignore_extra=False,
    )
    async def prefix_remove(self, ctx, prefix: Prefix):
        """ Removes a prefix from the list of custom prefixes.

        This is the inverse of the 'prefix add' command. You can use
        this command to remove prefixes from the default set as well.

        You must have manage server permission to use this command.
        """
        pass

    @prefix.command(name="clear", help="Removes all custom prefixes from the list")
    async def prefix_clear(self, ctx):
        """ Removes all custom previes from the list. 
        
        After this, the bot will listen to only metion prefixes.

        You must have manage server permission to use this command.
        """
        pass


def setup(bot):
    """ " Sets up the settings cog for the bot. """

    logger.info("Loading Settings Cog")
    bot.add_cog(SettingsCog(bot))


def teardown(bot):
    """ Tears down the settings cog for the bot. """
    logger.info("Unloading Settings Cog")
    bot.remove_cog("cogs.settings_cog")
