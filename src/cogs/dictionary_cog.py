# Third party imports
import discord
from discord.ext import commands, tasks

# Local applications
from util.logger import generate_logger

logger = generate_logger(__name__)


class DictionaryCog(commands.Cog, name="Dictionary"):
    def __init__(self, bot):
        """ Initialisation for DictionaryCog instance. """
        self.bot = bot
        self.printer.start()

    def create_embed(self):
        pass

    # Event Listeners
    @commands.Cog.listener()
    async def on_message(self, message):
        """ Called when a message is sent """

        if message.author != self.bot.user:
            # await message.channel.send("This is from dictionary")
            pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """ Called when a message is edited.
        
        Check if the message has a reaction object attached to it, run the equivalent command again (?)
        """

        prev_message = before
        next_message = after

        if (
            prev_message.author != self.bot.user
            and next_message.author != self.bot.user
        ):
            # await next_message.channel.send("This is from dictionary")
            pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """ Called when a message has a reaction added to it 
        
        If reactions are enabled and the text message is a single word 
        and a proper reactions is added to it, run the equivalent command
        """
        # await reaction.channel.send("This is from dictionary")
        pass

    @commands.Cog.listener()
    async def on_private_channel_delete(self, channel):
        """ Called whenever a private channel is deleted.
        
        If a channel is deleted, check if there's any config for it related
        to the dictionary functionality, and if so, remove any configuration.
        """
        pass

    @commands.Cog.listener()
    async def on_private_channel_update(self, before, after):
        """ Called whenever a private group DM is updated. e.g. changed name or topic 
        
        If a channel is updated and it has any configuration related to the dictionary
        functionality, update it with the new channel values. 
        """
        pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """ Callend when a Member leaves or joins a Guild 
        
        May not be used (?)
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

        May not be used (?)
        """
        pass

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        """ Called when a User updates their profile 
        
        This is called when one or more of the following things change:
        - avatar 
        - username
        - discriminator

        May not be used (?)
        """
        pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """ Callend when a Guildis removed from the Client 
        
        If the Client is removed from a Guild, if there's any config related to the dictionary
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
        """ Prints periodically a message. """
        # logger.warning("This is a warning from dictionary_cog")
        pass

    # Commands
    @commands.group(
        name="dictionary",
        aliases=["dict"],
        brief="Commands for dictionary search.",
        help="Commands for dictionary search.",
    )
    async def dictionary(self, ctx):
        """Commands for dictionary search. Use `~help dictionary` to view subcommands."""
        if ctx.invoked_subcommand is None:
            await ctx.send(
                f"Incorrect usage. Use {ctx.prefix}help dictionary for help."
            )
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

    @commands.guild_only()
    @dictionary.command(
        name="definition",
        aliases=["def"],
        brief="Embeds a message with a word definition.",
        help="Embeds a message with a word definition. The word search and the definition provided is done in english by default.",
    )
    async def dictionary_definition(
        self, ctx, word=None, word_language="english", definition_language="english"
    ):
        if word != None:
            await ctx.send("Definition for [word] is [definition].")
        else:
            await ctx.send("Couldn't find a definition for [word].")

    @commands.guild_only()
    @dictionary.command(
        name="noun",
        aliases=["n"],
        brief="Provides a list of nouns for an adjective.",
        help="Provides a list of nouns for an adjective. This is done in english by default.",
    )
    async def dictionary_noun(self, ctx):
        pass

    @commands.guild_only()
    @dictionary.command(
        name="adjective",
        aliases=["adj"],
        brief="Provides a list of adjectives for a noun.",
        help="Provides a list of adjectives for a noun. This is done in english by default.",
    )
    async def dictionary_adjective(self, ctx):
        pass

    @commands.guild_only()
    @dictionary.command(
        name="similar-spelling",
        aliases=["sim-spell"],
        brief="Provides a list of words that have a similar spelling.",
        help="Provides a list of words that have a similar spelling as the given word. This is done in english by default.",
    )
    async def dictionary_similar_spelling(self, ctx):
        pass

    @commands.guild_only()
    @dictionary.command(
        name="similar-sound",
        aliases=["sim-sound"],
        brief="Provides a list of words that have a similar sound.",
        help="Provides a list of words that have a similar sound as the given word. This is done in english by default.",
    )
    async def dictionary_similar_sound(self, ctx):
        pass

    @commands.guild_only()
    @dictionary.command(
        name="rhyme",
        brief="Provides a list of words that rhyme.",
        help="Provides a list of words that rhyme with the given word. This is done in english by default.",
    )
    async def dictionary_rhyme(self, ctx):
        pass

    @commands.guild_only()
    @dictionary.command(
        name="wotd",
        brief="Programs a quote of the day for the specified channels.",
        help="Programs a quote of the day for the specified channels. This is done in english by default.",
    )
    async def dictionary_wotd(self, ctx):
        pass

    @commands.guild_only()
    @dictionary.command(
        name="show-word",
        aliases=["gen-word"],
        brief="Shows a random word with its definition",
        help="Shows a random word with its definition. This is done in english by default.",
    )
    async def dictionary_generate_word(self, ctx):
        pass


def setup(bot):
    """ Setups up the dictionary cog for the bot. """
    logger.info("Loading Dictionary Cog")
    bot.add_cog(DictionaryCog(bot))


def teardown(bot):
    """ Tears down the dictionary cog for the bot. """
    logger.info("Unloading Dictionary Cog")
    bot.remove_cog("cogs.dictionary_cog")
