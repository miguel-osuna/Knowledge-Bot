# Standard library imports
import typing
import json
import os
from os.path import dirname, abspath, join
import pdb

# Third party imports
import discord
from discord.ext import commands, tasks

# Local applications
from util.logger import generate_logger


BASE_PROJECT_PATH = dirname(dirname(dirname((abspath(__file__)))))
LANGUAGES_PATH = join(BASE_PROJECT_PATH, "data", "input", "langs.json")

logger = generate_logger(__name__)


class Language:
    """ Language class that represents a language used for translation. """

    def __init__(self, language_name, language_code, country_flag):
        """ Initialization for Language instance. """
        self.language_name = language_name.lower()
        self.language_code = language_code.lower()
        self.country_flags = country_flag.lower()

    def __str__(self):
        """ String representation of the object. """
        return f"Language: {self.language_name}, Code: {self.language_code}, Flags: {self.country_flags}"

    def __repr__(self):
        """ Object representation. """
        return f"Language: {self.language_name}, Code: {self.language_code}, Flags: {self.country_flags}"

    def __key(self):
        """ Base key for equality and hash methods. """
        return (self.language_name, self.language_code, self.country_flags)

    def __eq__(self, other):
        """ Check if a two languages are the same. """
        return self.__key() == other.__key()

    def __hash__(self):
        """ Returns the hash value of an instance. """
        return hash(self.__key())

    # Add class converter for discord arguments


class Translate(commands.Cog):
    def __init__(self, bot):
        """ Initialization for Translate cog instance. """
        self.bot = bot
        self.printer.start()
        self.langs_data = None
        self.default_language = Language("English", "en", "🇺🇸")
        self.supported_languages = self.load_languages()

    def load_languages(self):
        """ Load the available languages for translation. """
        langs = []

        try:
            with open(LANGUAGES_PATH) as json_file:
                data = json.load(json_file)
                self.langs_data = data

                for language in data["languages"]:
                    new_lang = Language(
                        language["name"],
                        language["languageCode"],
                        language["countryFlag"],
                    )
                    langs.append(new_lang)
                    print(new_lang)

        except (FileNotFoundError, IOError) as e:
            logger.error(e)

        return langs

    def is_language_supported(self, language):
        if isinstance(language, Language):
            return language in self.supported_languages
        return False

    def create_language(self, language_text):
        """ Creates a Language class instance by using the langs data file. """
        data = self.langs_data
        language_instance = None

        for language in data["languages"]:
            if (
                language["name"] == language_text
                or language["languageCode"] == language_text
                or language_text in language["countryFlag"]
            ):
                language_instance = Language(
                    language["name"], language["languageCode"], language["countryFlag"]
                )

        return language_instance

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
    @commands.group(
        name="translate", aliases=["t"], help="Commands for text translation."
    )
    async def translate(self, ctx):
        """ Commands for text translation. Use `~help translate` to view subcommands."""

        if ctx.invoked_subcommand is None:
            await ctx.send(f"Incorrect usage. Use {ctx.prefix}help translate for help.")
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

    @translate.command(
        name="list",
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
    async def translate_text(self, ctx, languages=None, *, text=None):
        if languages is not None and text is not None:
            # Check if theres a colon present in the languages specified by the user
            try:
                from_language, to_languages = languages.split(":")

            # If not from_language was specified, use the channels default
            except ValueError as err:
                logger.debug(err)
                from_language = [self.default_language.language_name]
                to_languages = languages

            # Separate the translation languages into their own list of strings
            try:
                from_language = from_language.split(",")
                to_languages = to_languages.split(",")

            except AttributeError as err:
                logger.debug(err)
                await ctx.send("Please provide the correct arguments.")

            # Check if there is just one language to translate
            if len(from_language) > 1:
                await ctx.send("Please specify a single language to translate.")

            else:
                # Create Language instances to ease their comparisson
                from_language = list(map(self.create_language, from_language))
                to_languages = list(map(self.create_language, to_languages))

                are_languages_valid = True
                languages_repeat = False

                # Check that the languages passed are valid and available
                for lang in from_language:
                    if lang is None:
                        are_languages_valid = False
                        break

                for lang in to_languages:
                    if lang is None:
                        are_languages_valid = False
                        break

                # Check that from_language is not included in to_languages
                for from_lang in from_language:
                    for to_lang in to_languages:
                        if to_lang == from_lang:
                            languages_repeat = True
                            break

                # Send message if any of the languages is not valid
                if not are_languages_valid:
                    await ctx.send("Please provide supported languages.")

                # Send message if from_language is found inside to_languages
                if languages_repeat:
                    await ctx.send("Please make sure to not repeat any languages.")

                if are_languages_valid and not languages_repeat:
                    # Remove any repeated languages to avoid over translations
                    to_languages = list(set(to_languages))
                    print("From language", from_language)
                    print("To languages", to_languages)

                    # Perform translation

                    # Send message with the translation
                    await ctx.send(f"{ctx.author}: {text}")

        else:
            await ctx.send("Please provide the correct arguments.")

    @translate.command(
        name="default",
        aliases=["dflt"],
        brief="Sets default language for specified channels.",
        help="Sets default language for specified channels.",
    )
    async def translate_default(
        self,
        ctx,
        default_language=None,
        channels: commands.Greedy[discord.TextChannel] = None,
    ):
        if default_language is not None and channels is not None:

            # Generate a Language class instance
            def_lang = self.create_language(default_language)
            channel_str = ", ".join(["#" + channel.name for channel in channels])

            # Check if the language is supported
            if not self.is_language_supported(def_lang):
                await ctx.send("Please specify a supported language.")

            else:
                # Setup the language on the database for each one of the channels

                # Notify the member that the default language has been setup
                await ctx.send(
                    f"Default {def_lang.language_name} language setup for channel/s {channel_str}."
                )

        else:
            await ctx.send(f"Couldn't configure default language for server.")

    @translate.command(
        name="default-server",
        aliases=["dflt-svr"],
        brief="Sets default language for the whole server.",
        help="Sets default language for the whole server. This overwrites any default language preset on the channels.",
    )
    async def translate_default_server(self, ctx, default_language=None):
        if default_language is not None:
            # Generate a Language class instance
            def_lang = self.create_language(default_language)
            guild_str = ctx.guild.name
            print(def_lang)

            if not self.is_language_supported(def_lang):
                await ctx.send("Please specify a supported language.")

            else:
                # Setup the language on the database for the server, which means that you also
                # need to replace the languages of the channels too

                # Notify the member that the default language has been setup
                await ctx.send(
                    f"{def_lang} setup as default language for {guild_str} server."
                )

        else:
            await ctx.send(f"Couldn't configure default language for server.")

    @translate.command(
        name="auto",
        brief="Sets default language for the whole server.",
        help="Enables or Disables automatic translation for specified channels. Translates the specified languages into the channel's default languages.",
    )
    async def translate_auto(
        self,
        ctx,
        status=None,
        languages=None,
        channels: commands.Greedy[discord.TextChannel] = None,
    ):
        if status is not None and channels is not None:
            # Parse languages and separate them to create Language class instances
            status = status.lower()
            languages = languages.split(",")
            setup_languages = list(map(self.create_language, languages))
            channel_str = ", ".join(["#" + channel.name for channel in channels])

            # Check if the languages provided are valid
            are_languages_valid = True
            for lang in setup_languages:
                if not lang.is_language_supported(lang):
                    are_languages_valid = False

            if status != "enable" or status != "disable":
                await ctx.send(f"Please provide correct status.")

            elif not are_languages_valid:
                await ctx.send(f"Please specify supported languages.")

            # Everything is valid
            else:
                # Get channels from the server

                # Configure the auto translation for the channels

                await ctx.send(
                    f"{languages} auto translation {status}d for channels {channel_str}."
                )
        else:
            await ctx.send(f"Couldn't configure auto translation.")

    @translate.command(
        name="auto-server",
        brief="Enables or Disables automatic translation for the server",
        help="Enables or Disables automatic translation for the server. Translates the specified languages into the channel's default languages. This overwrites any default language preset on the channels.",
    )
    async def translate_auto_server(self, ctx, status=None, languages=None):
        if status is not None and languages is not None:
            # Parser languages and separate them to create Language class instances
            status = status.lower()
            languages = languages.split(",")
            setup_languages = list(map(self.create_language, languages))
            guild_str = ctx.guild.name

            are_languages_valid = True
            for lang in setup_languages:
                if not lang.is_language_supported(lang):
                    are_languages_valid = False

            # Check if the status is different from enable or disable
            if status != "enable" or status != "disable":
                await ctx.send(f"Please provide correct status.")

            # Check if all the languages are supported languages
            elif not are_languages_valid:
                await ctx.send(f"Please specify supported languages.")

            # Everything is valid
            else:
                # Get server

                # Configure auto translation for the whole server, and therefore, for all the channels
                # This overwrites any auto translation that was setup previously on a channel

                await ctx.send(
                    f"{setup_languages} auto translation {status}d for {guild_str} server."
                )

        else:
            await ctx.send("Couldn't configure auto translation for the server.")

    @translate.command(
        name="auto-user",
        brief="Enables or Disables automatic translation for specified users.",
        help="Enables or Disables automatic translation for specified users.",
    )
    async def translate_auto_user(
        self,
        ctx,
        status=None,
        to_language=None,
        members: commands.Greedy[discord.Member] = None,
    ):
        if status is not None and to_language is not None and members is not None:

            setup_language = self.create_language(to_language)
            member_str = ", ".join(["@" + member.display_name for member in members])

            await ctx.send(
                f"{setup_language} auto translation {status}d for user/s {member_str}."
            )

            # Check if the status is different from enable or disable
            if status != "enable" or status != "disable":
                await ctx.send(f"Please provide correct status.")

            # Check if all the languages are supported languages
            elif not are_languages_valid:
                await ctx.send(f"Please specify supported languages.")

        else:
            await ctx.send("Couldn't configure auto translation for the users.")

    @translate.command(
        name="reaction",
        brief="Enables or Disables translation by country flag reactions.",
        help="Enables or Disables translation by country flag reactions.",
    )
    async def translate_reaction(self, ctx, status=None, *, arg):
        # 'arg' include languages and channels=discord.TextChannel
        if status is not None and arg is not None:
            await ctx.send(
                "Reaction translation [enabled/disabled] for channels #[channel] and #[channel]."
            )
        else:
            await ctx.send(
                "Couldn't [enable/disable] reaction translation for channels #[channel] and #[channel]"
            )

    @translate.command(name="detect", help="Detects the language of a given message.")
    async def translate_detect(self, ctx, *, text):
        if text is not None:
            await ctx.send("[language] detected on message [text].")

        else:
            await ctx.send("Couldn't detect language on message [text].")

    @translate.command(
        name="status",
        brief="Shows the status of the server, channels or users specified",
        help="Shows the status of the server, channels or users specified.",
    )
    async def translate_status(self, ctx, *, arg):
        # 'arg' can be server, channels: discord.TextChannel or users: discord.User
        if arg is not None:
            await ctx.send("Status for [server/channel/user]")

        else:
            await ctx.send("Couldn't get status for [server/channel/user]")


def setup(bot):
    bot.add_cog(Translate(bot))
