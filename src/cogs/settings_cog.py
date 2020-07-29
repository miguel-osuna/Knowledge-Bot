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

    # Tasks
    @tasks.loop(seconds=10.0)
    async def printer(self):
        logger.warning("This is a warning from settings_cog")

    # Commands
    @commands.group(
        name="settings", aliases=["stgs"], help="Commands for bot server settings."
    )
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
        brief="Sets the bot prefix character",
        help="Sets the bot prefix character. The default bot prefix is `=`.",
    )
    async def settings_prefix(self, ctx, prefix=None):
        if prefix != None:
            await ctx.send("Prefix `[prefix]` setup for bot commands.")
        else:
            await ctx.send("Couldn't setup `[prefix]` as the bots command prefix.")


def setup(bot):
    bot.add_cog(Settings(bot))
