# Third party imports
import discord
from discord.ext import commands, tasks

# Local applications
from util.logger import generate_logger

logger = generate_logger(__name__)


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

    # Tasks
    @tasks.loop(seconds=10.0)
    async def printer(self):
        # logger.warning("This is a warning from settings_cog")
        pass

    # Commands
    @commands.is_owner()
    @commands.command(name="load", help="Loads a specified extension/cog", hidden=True)
    async def load_cog(self, ctx, *, cog: str):
        """ Command which loads a module. """
        try:
            self.bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            await ctx.send(f"**`ERROR`:** {type(e).__name__} - {e}")
        else:
            await ctx.send(f"**`SUCCESS`**")

    @commands.is_owner()
    @commands.command(
        name="unload", help="Unloads a specified extension/cog", hidden=True
    )
    async def unload_cog(self, ctx, *, cog: str):
        """ Command which unloads a module. """
        try:
            self.bot.unload_extension(f"cogs.{cog}")
        except Exception as e:
            await ctx.send(f"**`ERROR`:** {type(e).__name__} - {e}")
        else:
            await ctx.send(f"**`SUCCESS`**")

    @commands.is_owner()
    @commands.command(
        name="reload", help="Reloads a specific extension/cog", hidden=True
    )
    async def reload_cog(self, ctx, *, cog: str):
        """ Command which reloads a module. """
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            self.bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            await ctx.send(f"**`ERROR`:** {type(e).__name__} - {e}")
        else:
            await ctx.send(f"**`SUCCESS`**")

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

    @settings.command(
        name="prefix",
        brief="Sets the bot prefix character",
        help="Sets the bot prefix character. The default bot prefix is `=`.",
    )
    async def settings_prefix(self, ctx, prefix: str = None):
        if prefix != None:
            # Get server from the database

            # Set prefix for the server on the database
            await ctx.send(f"Prefix `{prefix}` setup for bot commands.")
        else:
            await ctx.send(f"Couldn't setup prefix.")

    # Command Error Handling
    @settings_prefix.error
    async def settings_prefix_error(self, ctx, error):
        pass


def setup(bot):
    """" Sets up the settings cog for the bot. """
    logger.info("Loading Settings Cog")
    bot.add_cog(SettingsCog(bot))


def teardown(bot):
    """ Tears down the settings cog for the bot. """
    logger.info("Unloading Settings Cog")
    bot.remove_cog("cogs.settings_cog")
