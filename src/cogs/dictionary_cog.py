# Third party imports
import discord
from discord.ext import commands, tasks

# Local applications
from util.logger import generate_logger

logger = generate_logger(__name__)


class DictionaryCog(commands.Cog):
    def __init__(self, bot):
        """ Initialisation for DictionaryCog instance. """
        self.bot = bot
        self.printer.start()

    # Events
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
        """ Prints periodically a message. """
        logger.warning("This is a warning from dictionary_cog")

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

    @dictionary.command(
        name="noun",
        aliases=["n"],
        brief="Provides a list of nouns for an adjective.",
        help="Provides a list of nouns for an adjective. This is done in english by default.",
    )
    async def dictionary_noun(self, ctx):
        pass

    @dictionary.command(
        name="adjective",
        aliases=["adj"],
        brief="Provides a list of adjectives for a noun.",
        help="Provides a list of adjectives for a noun. This is done in english by default.",
    )
    async def dictionary_adjective(self, ctx):
        pass

    @dictionary.command(
        name="similar-spelling",
        aliases=["sim-spell"],
        brief="Provides a list of words that have a similar spelling.",
        help="Provides a list of words that have a similar spelling as the given word. This is done in english by default.",
    )
    async def dictionary_similar_spelling(self, ctx):
        pass

    @dictionary.command(
        name="similar-sound",
        aliases=["sim-sound"],
        brief="Provides a list of words that have a similar sound.",
        help="Provides a list of words that have a similar sound as the given word. This is done in english by default.",
    )
    async def dictionary_similar_sound(self, ctx):
        pass

    @dictionary.command(
        name="rhyme",
        brief="Provides a list of words that rhyme.",
        help="Provides a list of words that rhyme with the given word. This is done in english by default.",
    )
    async def dictionary_rhyme(self, ctx):
        pass

    @dictionary.command(
        name="wotd",
        brief="Programs a quote of the day for the specified channels.",
        help="Programs a quote of the day for the specified channels. This is done in english by default.",
    )
    async def dictionary_wotd(self, ctx):
        pass

    @dictionary.command(
        name="show-word",
        aliases=["gen-word"],
        brief="Shows a random word with its definition",
        help="Shows a random word with its definition. This is done in english by default.",
    )
    async def dictionary_generate_word(self, ctx):
        pass

    # Command Error Handling
    @dictionary_definition.error
    async def dictionary_definition_error(self, ctx, error):
        pass

    @dictionary_noun.error
    async def dicitonary_noun_error(self, ctx, error):
        pass

    @dictionary_adjective.error
    async def dictionary_adjective_error(self, ctx, error):
        pass

    @dictionary_similar_spelling.error
    async def dictionary_similar_spelling_error(self, ctx, error):
        pass

    @dictionary_similar_sound.error
    async def dictionary_similar_sound_error(self, ctx, error):
        pass

    @dictionary_rhyme.error
    async def dictionary_rhyme_error(self, ctx, error):
        pass

    @dictionary_wotd.error
    async def dictionary_wotd_error(self, ctx, error):
        pass

    @dictionary_generate_word.error
    async def dictionary_generate_word_error(self, ctx, error):
        pass


def setup(bot):
    """ Setups up the dictionary cog for the bot. """
    bot.add_cog(DictionaryCog(bot))
