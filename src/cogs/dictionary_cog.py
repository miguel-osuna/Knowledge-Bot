from datetime import datetime

import discord
from discord.ext import commands

from util import (
    generate_logger,
    Pages,
    get_definition,
    get_synonyms,
    get_antonyms,
    get_similar_words,
    get_rhymes,
    get_word_of_the_day,
    get_random_word,
)

logger = generate_logger(__name__)


class WordPaginator(Pages):
    """Word of the Day Status Paginator."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DictionaryCog(commands.Cog, name="Dictionary"):
    def __init__(self, bot):
        """Initialisation for DictionaryCog instance."""
        self.bot = bot

    def create_definition_embed(self, word, definition):
        """Creates an embed to show a word definition."""
        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.title = "📖 Definition"
        embed.description = f"**{word}**\n*noun* [C]\n*```{definition}```*"
        embed.timestamp = datetime.utcnow()
        return embed

    def create_synonym_embed(self, word, synonyms_list):
        """Creates an embed to show synonyms of a word."""
        synonyms_string = ", ".join([synonym for synonym in synonyms_list])
        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.title = f"📖 Synonyms for *{word}*"
        embed.description = (
            f"Found **{len(synonyms_list)}** synonyms:\n```{synonyms_string}```"
        )
        embed.timestamp = datetime.utcnow()
        return embed

    def create_antonym_embed(self, word, antonyms_list):
        """Creates an embed to show antonyms of a word."""
        antonyms_string = ", ".join([antonym for antonym in antonyms_list])
        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.title = f"📖 Antonyms for *{word}*"
        embed.description = (
            f"Found **{len(antonyms_list)}** antonyms:\n```{antonyms_string}```"
        )
        embed.timestamp = datetime.utcnow()
        return embed

    def create_similar_embed(self, word, similar_list):
        """Creates an embed to show words with similar sound or spelling (homonyms/homographs)."""

        similar_string = ""
        for index, value in enumerate((similar_list)):
            similar_string += "{}. {}\n".format(index + 1, value["definition"])

        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.title = f"📖 Homonyms for *{word}*"
        embed.description = f"Found **{len(similar_list)}** similar sounds or spelling words:\n```{similar_string}```"
        embed.timestamp = datetime.utcnow()
        return embed

    def create_rhyme_embed(self, word, rhyme_list):
        """Creates an embed to show words that rhyme with a word."""
        rhyme_string = ", ".join([rhyme for rhyme in rhyme_list])
        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.title = f"📖 Rhymes for *{word}*"
        embed.description = (
            f"Found **{len(rhyme_list)}** rhymes:\n ```{rhyme_string}```"
        )
        embed.timestamp = datetime.utcnow()
        return embed

    def create_error_embed(self, message):
        """Creates an embed to display an error message."""
        embed = discord.Embed(color=discord.Color.red())
        embed.title = message
        return embed

    # Class Methods
    async def cog_before_invoke(self, ctx):
        """A special method that acts as a cog local pre-invoke hook."""
        await ctx.trigger_typing()
        return await super().cog_before_invoke(ctx)

    async def cog_after_invoke(self, ctx):
        """A special method that acts as a cog local post-invoek hook."""
        return await super().cog_after_invoke(ctx)

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
            await ctx.channel.send(
                f"Incorrect usage. Use `{ctx.prefix}help dictionary` for help."
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
        help="Embeds a message with a word definition.",
    )
    async def dictionary_definition(self, ctx, word=None):
        """Embeds a message with a word definition."""
        try:
            if word is not None:
                definition = get_definition(word)[0]

                # Check if there is a definition for the word
                if definition:
                    embed = self.create_definition_embed(word, definition)
                    await ctx.channel.send(embed=embed)
                else:
                    raise Exception
            else:
                raise Exception
        except:
            message = f"Sorry, I could not find a definition for `{word}`."
            logger.error(message)
            embed = self.create_error_embed(message)
            await ctx.channel.send(embed=embed)

    @commands.guild_only()
    @dictionary.command(
        name="synonym",
        aliases=["syn"],
        brief="Provides a list of synonyms for the word given.",
        help="Provides a list of synonyms for the word given.",
    )
    async def dictionary_synonym(self, ctx, word=None):
        """Provides a list of synonyms for the word given."""
        try:
            if word is not None:
                synonyms = get_synonyms(word)

                # Check if there are synonyms for the word
                if synonyms:
                    embed = self.create_synonym_embed(word, synonyms)
                    await ctx.channel.send(embed=embed)
                else:
                    raise Exception
            else:
                raise Exception
        except:
            message = f"Sorry, I could not find any synonyms for `{word}`."
            logger.error(message)
            embed = self.create_error_embed(message)
            await ctx.channel.send(embed=embed)

    @commands.guild_only()
    @dictionary.command(
        name="antonym",
        aliases=["ant"],
        brief="Provides a list of antonyms for the word given.",
        help="Provides a list of antonyms for the word given.",
    )
    async def dictionary_antonym(self, ctx, word=None):
        """Provides a list of antonyms for the word given."""
        try:
            if word is not None:
                synonyms = get_antonyms(word)

                # Check if there are synonyms for the word
                if synonyms:
                    embed = self.create_antonym_embed(word, synonyms)
                    await ctx.channel.send(embed=embed)
                else:
                    raise Exception
            else:
                raise Exception
        except:
            message = f"Sorry, I could not find any antonyms for `{word}`."
            logger.error(message)
            embed = self.create_error_embed(message)
            await ctx.channel.send(embed=embed)

    @commands.guild_only()
    @dictionary.command(
        name="similar",
        aliases=["sim"],
        brief="Provides a list of words that have similar sound or spelling as the given word. (homonyms/homographs)",
        help="Provides a list of words that have similar sound or spelling as the given word (homonyms/homographs). This is done in english by default.",
    )
    async def dictionary_similar(self, ctx, word=None):
        """Provides a list of words that have similar sound or spelling as the given word (homonyms/homographs)."""
        try:
            if word is not None:
                similar_words = get_similar_words(word)

                # Check if there are similar words for the given word
                if similar_words:
                    embed = self.create_similar_embed(word, similar_words)
                    await ctx.channel.send(embed=embed)
                else:
                    raise Exception
            else:
                raise Exception
        except:
            message = f"Sorry, I could not find similar sounds or spelling words for `{word}`."
            logger.error(message)
            embed = self.create_error_embed(message)
            await ctx.channel.send(embed=embed)

    @commands.guild_only()
    @dictionary.command(
        name="rhyme",
        brief="Provides a list of words that rhyme.",
        help="Provides a list of words that rhyme with the given word. This is done in english by default.",
    )
    async def dictionary_rhyme(self, ctx, word=None):
        """Provides a list of words that rhyme with the given word."""
        try:
            if word is not None:
                rhymes = get_rhymes(word)
                if rhymes:
                    embed = self.create_rhyme_embed(word, rhymes)
                    await ctx.channel.send(embed=embed)
                else:
                    raise Exception
            else:
                raise Exception
        except:
            message = f"Sorry, I could not find any rhymes for `{word}`."
            logger.error(message)
            embed = self.create_error_embed(message)
            await ctx.channel.send(embed=embed)

    @commands.guild_only()
    @dictionary.command(
        name="wotd",
        brief="Shows the word of the day.",
        help="Shows the word of the day.",
    )
    async def dictionary_word_of_the_day(self, ctx):
        """Shows the word of the day."""
        try:
            word, definitions = get_word_of_the_day()
            embed = self.create_definition_embed(word, definitions[0])
            await ctx.channel.send(embed=embed)
        except:
            message = "Sorry, could not get word of the day."
            logger.error(message)
            embed = self.create_error_embed(message)
            await ctx.channel.send(embed=embed)

    @commands.guild_only()
    @dictionary.command(
        name="random",
        aliases=["rnd"],
        brief="Shows a random word with its definition",
        help="Shows a random word with its definition.",
    )
    async def dictionary_random_word(self, ctx):
        """Shows a random word with its definition."""
        # Get a random word and its definition from the database
        try:
            word = get_random_word()
            definition = get_definition(word)[0]
            embed = self.create_definition_embed(word, definition)
            await ctx.channel.send(embed=embed)
        except:
            message = f"Sorry, could not get random word."
            logger.error(message)
            embed = self.create_error_embed(message)
            await ctx.channel.send(embed=embed)


def setup(bot):
    """Setups up the dictionary cog for the bot."""
    logger.info("Loading Dictionary Cog")
    bot.add_cog(DictionaryCog(bot))


def teardown(bot):
    """Tears down the dictionary cog for the bot."""
    logger.info("Unloading Dictionary Cog")
    bot.remove_cog("cogs.dictionary_cog")
