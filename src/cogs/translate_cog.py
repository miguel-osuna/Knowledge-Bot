import json
from datetime import datetime

import discord
from discord.ext import commands

from util import generate_logger, Pages, detect_language, list_languages, translate_text
from config import LANGUAGES_PATH

logger = generate_logger(__name__)


class Language:
    """Language class that represents a language used for translation."""

    def __init__(self, language_name, language_code, country_flag):
        """Initialisation for Language instance."""
        self.language_name = language_name.lower()
        self.language_code = language_code.lower()
        self.country_flags = country_flag.lower()

    def __str__(self):
        """String representation of the object."""
        return f"Language: {self.language_name}, Code: {self.language_code}, Flags: {self.country_flags}"

    def __repr__(self):
        """Object representation."""
        return f"Language: {self.language_name}, Code: {self.language_code}, Flags: {self.country_flags}"

    def __key(self):
        """Base key for equality and hash methods."""
        return (self.language_name, self.language_code, self.country_flags)

    def __eq__(self, other):
        """Check if a two languages are the same."""
        return self.__key() == other.__key()

    def __hash__(self):
        """Returns the hash value of an instance."""
        return hash(self.__key())


class TranslateCog(commands.Cog, name="Translate"):
    """Bot translation cog."""

    def __init__(self, bot):
        """Initialisation for TranslateCog instance."""
        self.bot = bot
        self.langs_data = None
        self.default_language = Language("English", "en", "🇺🇸")
        self.supported_languages = self.load_languages()

    def load_languages(self):
        """Load the available languages for translation."""
        langs = []

        try:
            with open(LANGUAGES_PATH + ".json") as json_file:
                data = json.load(json_file)
                self.langs_data = data

                for language in data["languages"]:

                    new_lang = Language(
                        language["name"],
                        language["languageCode"],
                        language["countryFlag"],
                    )
                    langs.append(new_lang)

        except (FileNotFoundError, IOError) as e:
            logger.error(e)

        return langs

    def is_language_supported(self, language):
        if isinstance(language, Language):
            return language in self.supported_languages
        return False

    def create_language(self, language_text):
        """Creates a Language class instance by using the langs data file."""
        data = self.langs_data
        language_instance = None

        for language in data["languages"]:
            if (
                language["name"] == language_text.capitalize()
                or language["languageCode"] == language_text.lower()
                or language_text in language["countryFlag"]
            ):
                language_instance = Language(
                    language["name"], language["languageCode"], language["countryFlag"]
                )

        return language_instance

    def create_translate_list_embed(self, language_list):
        """Creates embed to show list of supported languages."""

        # Generate value strings for embed
        name_string = ""
        code_string = ""
        country_flags_string = ""

        for language in language_list:
            name_string += language.language_name + "\n"
            code_string += language.language_code + "\n"
            country_flags_string += language.country_flags[:3] + "\n"

        # Create Discord embed
        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.title = "🌎 Supported Languages"
        embed.description = f"This is a list of all the supported languages with their respective name, language code and country flags.\n"
        embed.add_field(name="Name", value=f"{name_string}")
        embed.add_field(name="Language Code", value=f"{code_string}")
        embed.add_field(name="Country Flags", value=f"{country_flags_string}")
        embed.timestamp = datetime.utcnow()

        return embed

    def create_translate_text_embed(
        self, author_name, author_img, original_text, translated_text
    ):
        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.set_author(name=author_name, icon_url=author_img)
        embed.description = f"**{translated_text}**\n*{original_text}*"
        embed.timestamp = datetime.utcnow()
        return embed

    def create_translate_detect_embed(self, message, language_name, language_code):
        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.title = "🔎 Language Detection"
        embed.description = f"Language Detected: **{language_name}** (***{language_code}***)\n\n*{message}*"
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
        # Setup database connections
        await ctx.trigger_typing()
        return await super().cog_before_invoke(ctx)

    async def cog_after_invoke(self, ctx):
        """A special method that acts as a cog local post-invoek hook."""
        return await super().cog_after_invoke(ctx)

    # Commands
    @commands.group(
        name="translator", aliases=["t"], help="Commands for text translation."
    )
    async def translator(self, ctx):
        """Commands for text translation. Use `~help translator` to view subcommands."""

        if ctx.invoked_subcommand is None:
            await ctx.channel.send(
                f"Incorrect usage. Use `{ctx.prefix}help translator` for help."
            )
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

    @translator.command(
        name="list",
        aliases=["ls"],
        brief="Sends a list of all supported languages.",
        help="Sends a list of all supported languages.",
    )
    async def translate_list(self, ctx):
        """Sends a list of all supported languages."""
        # Send an embed to the author of the message
        embed = self.create_translate_list_embed(self.supported_languages)
        await ctx.author.send(embed=embed)

    @commands.guild_only()
    @translator.command(
        name="text",
        aliases=["txt"],
        brief="Translates a sentence from one language to another.",
        help="Translates a sentence from one language to another.",
    )
    async def translate_text(self, ctx, language=None, *, text: str = None):
        """Translate a sentence from one language to another."""
        try:
            if language is not None and text is not None:
                translation = translate_text(language, text)
                author_name = ctx.author.name
                author_img = ctx.author.avatar_url

                embed = self.create_translate_text_embed(
                    author_name, author_img, text, translation
                )
                await ctx.channel.send(embed=embed)

            else:
                raise Exception
        except:
            message = f"Sorry, I could not translate your text. Please make sure to provide a supported language."
            logger.error(message)
            embed = self.create_error_embed(message)
            await ctx.channel.send(embed=embed)

    @commands.guild_only()
    @translator.command(name="detect", help="Detects the language of a given message.")
    async def translate_detect(self, ctx, *, text: str = None):
        try:
            if text is not None:
                detected_language = detect_language(text)
                language = self.create_language(detected_language)
                embed = self.create_translate_detect_embed(
                    text, language.language_name, language.language_code
                )
                await ctx.channel.send(embed=embed)

            else:
                raise Exception

        except:
            message = "Sorry, I could not find any language for your text."
            logger.error(message)
            embed = self.create_error_embed(message)
            await ctx.channel.send(embed=embed)


def setup(bot):
    """Sets up the translate cog for the bot."""
    logger.info("Loading Translate Cog")
    bot.add_cog(TranslateCog(bot))


def teardown(bot):
    """Tears down the translate cog for the bot."""
    logger.info("Unloading Translate Cog")
    bot.remove_cog("cogs.translate_cog")
