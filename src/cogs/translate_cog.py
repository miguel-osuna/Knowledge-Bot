# Third party imports
import discord
from discord.ext import commands, tasks

# Local applications
from util.logger import generate_logger

logger = generate_logger(__name__)


class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.printer.start()

    # Events
    @commands.Cog.listener()
    async def on_message(self, message):
        """ Called when a message is sent 
        
        If the message sent was from a text channel, user or server configured, make sure
        to run the translate command with the configuration values as arguments along with the text from the message
        """

        if message.author != self.bot.user:
            # await message.channel.send("This is from translate")
            pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """ Called when a message is edited 
        
        If the message is updated, and it's on a text channel, from a user or server configured, delete the previous translation and 
        embed a new one with the modified data. 

        Also make sure to reset the reactions, so people can react to it again, without to unreact to it manually. (?)
        """

        prev_message = before
        next_message = after

        if (
            prev_message.author != self.bot.user
            and next_message.author != self.bot.user
        ):
            # await next_message.channel.send("This is from translate")
            pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """ Called when a message has a reaction added to it 
        
        First of all, check if the translations of the reaction are enabled on the whole server or on the
        channel the reaction was made. If so, check that the reaction is the appropiate one to translate the message.

        These translations by reaction are sent via DM to not clutter the text channel
        """
        # await reaction.channel.send("This is from translate")
        pass

    @commands.Cog.listener()
    async def on_private_channel_delete(self, channel):
        """ Called whenever a private channel is deleted 
        
        If a channel that was deleted had a configuration for the translation functionality, 
        make sure to also delete any values related. 
        """
        pass

    @commands.Cog.listener()
    async def on_private_channel_update(self, before, after):
        """ Called whenever a private group DM is updated. e.g. changed name or topic
        
        If the channel that was updated had a config for the translation functionality, make
        sure to also update the database with the newest values. 
        """
        pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """ Called when a Member leaves a Guild 
        
        If the member that was removed had any config for the translation functionality, make
        sure to also remove that from the database
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

        If the member that was updated had a config for the translation functionality, make 
        sure to also update the database with the newest values.
        """
        pass

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        """ Called when a User updates their profile 
        
        This is called when one or more of the following things change:
        - avatar 
        - username
        - discriminator

        If the user that was updated had a config for the translation functionality, make 
        sure to also update the database with the newest values. 
        """
        pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """ Callend when a Guildis removed from the Client 
        
        If the Client is removed from a Guild, if there's any config related to the translation
        functionality, also remove it.         
        """
        pass

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        """ Called when a Guild updates 
        
        If the Guild is updated, and it has a configuration related to the dictionary 
        functionality, update it with the new guild values.         
        """
        pass

    # Tasks
    @tasks.loop(seconds=10.0)
    async def printer(self):
        logger.warning("This is a warning from translate_cog")

    # Commands
    channel_default_language = "english"

    @commands.group(
        name="translate", aliases=["t"], help="Commands for text translation."
    )
    async def translate(self, ctx):
        """ Commands for text translation. Use `=help translate` to view subcommands."""

        if ctx.invoked_subcommand is None:
            await ctx.send(f"Incorrect usage. Use {ctx.prefix}help translate for help.")
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

    @translate.command(
        name="langs",
        aliases=["ls"],
        brief="Sends a list of a ll languages supported.",
        help="Sends a list of all languages supported.",
    )
    async def translate_langs(self, ctx):
        await ctx.send("These are all the languages supported.")

    @translate.command(
        name="text",
        aliases=["txt"],
        brief="Translates a sentence from one language to another",
        help="Translates a sentence from one language to another.",
    )
    async def translate_text(
        self,
        ctx,
        from_language=channel_default_language,
        to_language=None,
        *,
        text=None,
    ):
        if to_language != None and text != None:
            await ctx.send("Text translated.")

        else:
            await ctx.send("Couldn't translate language.")

    @translate.command(
        name="default",
        aliases=["dflt"],
        brief="Sets default language for specified channels.",
        help="Sets default language for specified channels.",
    )
    async def translate_default(
        self, ctx, default_language=None, *, channels: discord.TextChannel
    ):
        if default_language != None and channels != None:
            await ctx.send(
                "Default [language] language setup for channels #[channel name] and #[channel name]."
            )

        else:
            await ctx.send(
                "Couldn't setup default [language] language for channels #[channel name] and #[channel name]"
            )

    @translate.command(
        name="default-server",
        aliases=["dflt-svr"],
        brief="Sets default language for the whole server.",
        help="Sets default language for the whole server. This overwrites any default language preset on the channels.",
    )
    async def translate_default_server(self, ctx, default_language=None):
        if default_language != None:
            await ctx.send(
                "[default_language] setup as default language for [server name] server."
            )
        else:
            await ctx.send(
                "Couldn't setup [default_language] as default language for [server name] server."
            )

    @translate.command(
        name="auto",
        brief="Sets default language for the whole server.",
        help="Enables or Disables automatic translation for specified channels. Translates the specified languages into the channel's default languages.",
    )
    async def translate_auto(
        self, ctx, status=None, *, languages, channels=discord.TextChannel
    ):
        if status != None and languages != None and channels != None:
            await ctx.send(
                "[languages] auto translation [enabled/disabled] for channels #[channel] and #[channel]."
            )

        else:
            await ctx.send(
                "Couldn't [enable/disable] [languages] auto translation for channels #[channel] and #[channel]."
            )

    @translate.command(
        name="auto-server",
        brief="Enables or Disables automatic translation for the server",
        help="Enables or Disables automatic translation for the server. Translates the specified languages into the channel's default languages. This overwrites any default language preset on the channels.",
    )
    async def translate_auto_server(self, ctx, status=None, *, languages=None):
        if status != None and languages != None:
            await ctx.send(
                "[languages] auto translation [enabled/disabled] for [server name] server."
            )

        else:
            await ctx.send(
                "Couldn't [enable/disable] [languages] auto translation for [server name] server."
            )

    @translate.command(
        name="auto-user",
        brief="Enables or Disables automatic translation for specified users.",
        help="Enables or Disables automatic translation for specified users.",
    )
    async def translate_auto_user(
        self, ctx, status=None, to_language=None, *, users=discord.User
    ):
        if status != None and to_language != None and users != None:
            await ctx.send(
                "[language] auto translation [enabled/disabled] for users @[user] and @[user]."
            )

        else:
            await ctx.send(
                "Couldn't [enable/disable] [language] auto translation for users @[user] and @[user]."
            )

    @translate.command(
        name="reaction",
        brief="Enables or Disables translation by country flag reactions.",
        help="Enables or Disables translation by country flag reactions.",
    )
    async def translate_reaction(
        self, ctx, status=None, *, languages, channels=discord.TextChannel
    ):
        if status != None and languages != None and channels != None:
            await ctx.send(
                "Reaction translation [enabled/disabled] for channels #[channel] and #[channel]."
            )
        else:
            await ctx.send(
                "Couldn't [enable/disable] reaction translation for channels #[channel] and #[channel]"
            )

    @translate.command(name="detect", help="Detects the language of a given message.")
    async def translate_detect(self, ctx, *, text):
        if text != None:
            await ctx.send("[language] detected on message [text].")

        else:
            await ctx.send("Couldn't detect language on message [text].")

    @translate.command(
        name="status",
        brief="Shows the status of the server, channels or users specified",
        help="Shows the status of the server, channels or users specified.",
    )
    async def translate_status(
        self,
        ctx,
        *,
        server: discord.Guild,
        channels: discord.TextChannel,
        users: discord.User,
    ):
        if server != None and channels != None and users != None:
            await ctx.send("Status for [server/channel/user]")

        else:
            await ctx.send("Couldn't get status for [server/channel/user]")


def setup(bot):
    bot.add_cog(Translate(bot))
