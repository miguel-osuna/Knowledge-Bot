# Third party imports
import discord
from discord.ext import commands, tasks

# Local applications
from util.logger import generate_logger

logger = generate_logger(__name__)


class Dictionary(commands.Cog):
    def __init__(self, bot):
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
        """ Called when a message is edited """

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
        """ Called when a message has a reaction added to it """
        # await reaction.channel.send("This is from dictionary")
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
        """ Prints periodically a message. """
        logger.warning("This is a warning from dictionary_cog")

    # Commands
    @commands.group(name="dictionary", aliases=["dict"])
    async def dictionary(self, ctx):
        """Commands for dictionary search. Use `=help dictionary` to view subcommands."""
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
        help="Embeds message with word definition. The word search and the definition provided is done in english by default.",
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
        help="Provides with a list of nouns for the adjective specified. This is done in english by default.",
    )
    async def dictionary_nount(self, ctx):
        pass

    @dictionary.command(
        name="adjective",
        aliases=["adj"],
        help="Provides with a list of adjectives for noun specified. This is done in english by default.",
    )
    async def dictionary_adjective(self, ctx):
        pass

    @dictionary.command(
        name="similar-spelling",
        aliases=["sim-spell"],
        help="Provides with a list of words that have a similar spelling as the word specified. This is done in english by default.",
    )
    async def dictionary_similar_spelling(self, ctx):
        pass

    @dictionary.command(
        name="similar-sound",
        aliases=["sim-sound"],
        help="Provides with a list of words that have a similar sound as the word specified. This is done in english by default.",
    )
    async def dictionary_similar_sound(self, ctx):
        pass

    @dictionary.command(
        name="rhyme",
        help="Provides with a list of words that rhyme with the word specified. This is done in english by default.",
    )
    async def dictionary_rhyme(self, ctx):
        pass

    @dictionary.command(
        name="wotd",
        help="Programs a quote of the day for the specified channels. This is done in english by default.",
    )
    async def dictionary_wotd(self, ctx):
        pass

    @dictionary.command(
        name="generate-word",
        aliases=["gen-word"],
        help="Genererates random word with its definition. This is done in english by default.",
    )
    async def dictionary_generate_word(self, ctx):
        pass


def setup(bot):
    """ Setups up the dictionary cog for the bot. """
    bot.add_cog(Dictionary(bot))
