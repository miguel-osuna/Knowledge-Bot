# Standard library imports
import typing
import pytz
from datetime import datetime

# Third party imports
import discord
from discord.ext import commands, tasks

# Local applications
from util.logger import generate_logger
from paginator import Pages

logger = generate_logger(__name__)


class WordPaginator(Pages):
    """ Word of the Day Status Paginator. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DictionaryCog(commands.Cog, name="Dictionary"):
    def __init__(self, bot):
        """ Initialisation for DictionaryCog instance. """
        self.bot = bot
        self.printer.start()

    def create_definition_embed(self, word, definition):
        """ Creates an embed to show a word definition. """
        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.title = "📖 Definition"
        embed.description = f"**{word}**\n*noun* [C]\n*```{definition}```*"
        embed.timestamp = datetime.utcnow()
        return embed

    def create_synonym_embed(self, word, synonyms_list):
        """ Creates an embed to show synonyms of a word. """
        synonyms_string = ", ".join([synonym for synonym in synonyms_list])
        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.title = f"📖 Synonyms for *{word}*"
        embed.description = (
            f"Found **{len(synonyms_list)}** synonyms:\n```{synonyms_string}```"
        )
        embed.timestamp = datetime.utcnow()
        return embed

    def create_antonym_embed(self, word, antonyms_list):
        """ Creates an embed to show antonyms of a word. """
        antonyms_string = ", ".join([antonym for antonym in antonyms_list])
        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.title = f"📖 Antonyms for *{word}*"
        embed.description = (
            f"Found **{len(antonyms_list)}** antonyms:\n```{antonyms_string}```"
        )
        embed.timestamp = datetime.utcnow()
        return embed

    def create_similar_embed(self, word, similar_list):
        """ Creates an embed to show words with similar sound or spelling (homonyms/homographs). """

        similar_string = ""
        for index, value in enumerate((similar_list)):
            similar_string += "{}. {}\n".format(index + 1, value["definition"])

        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.title = f"📖 Homonyms for *{word}*"
        embed.description = f"Found **{len(similar_list)}** similar sounds or spelling words:\n```{similar_string}```"
        embed.timestamp = datetime.utcnow()
        return embed

    def create_rhyme_embed(self, word, rhyme_list):
        """ Creates an embed to show words that rhyme with a word. """
        rhyme_string = ", ".join([rhyme for rhyme in rhyme_list])
        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.title = f"📖 Rhymes for *{word}*"
        embed.description = (
            f"Found **{len(rhyme_list)}** rhymes:\n ```{rhyme_string}```"
        )
        embed.timestamp = datetime.utcnow()
        return embed

    def create_word_of_the_day_embed(self, status, channels, time, language):
        """ Creates an embed to to notice the user when a word of the day is programmed. """
        embed = discord.Embed(
            title="📖 Word of the Day Setup", color=discord.Color.dark_purple()
        )

        embed.add_field(name="❓ Status", value=f"{status}\u200B\n", inline=False)
        embed.add_field(name="💬 Channels", value=f"{channels}\u200B\n", inline=False)
        embed.add_field(name="⌚ Time", value=f"{time}\u200B", inline=False)
        embed.add_field(name="🌎 Language", value=f"{language}\u200B", inline=False)
        embed.timestamp = datetime.utcnow()

        return embed

    def create_word_status_embed(self):
        """ Creates a paginator embed to show the word of the day status. """
        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.title = "📖 Word of the Day Status"
        embed.timestamp = datetime.utcnow()
        return embed

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
        help="Embeds a message with a word definition. The word and the definition provided are done in english by default.",
    )
    async def dictionary_definition(
        self, ctx, word=None, word_language="english", definition_language="english"
    ):
        """ Embeds a message with a word definition. 
        
        The word and the definition provided are done in english by default. 
        """
        if word != None:

            # Use function to check if the language is valid
            is_word_language_valid = True

            # Use function to check if the language is valid
            is_definition_language_valid = True

            if not is_word_language_valid or not is_definition_language_valid:
                await ctx.send("Please provide supported languages.")

            # Languages provided are valid
            else:

                # Check if the word exists
                is_word_valid = True

                if is_word_valid:
                    # Get the word definition for the embed

                    definition = "An autonomous program on a network (especially the Internet) that can interact with computer systems or users, especially one designed to respond or behave like a player in an adventure game."

                    embed = self.create_definition_embed(word, definition)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"Sorry, I couldn't find a definition for `{word}`.")

        else:
            await ctx.send("Sorry, couldn't find a definition.")

    @commands.guild_only()
    @dictionary.command(
        name="synonym",
        aliases=["syn"],
        brief="Provides a list of synonyms for the word given.",
        help="Provides a list of synonyms for the word given. This is done in english by default.",
    )
    async def dictionary_synonym(self, ctx, word=None):
        """ Provides a list of synonyms for the word given. 
        
        This is done in english by default. 
        """
        if word is not None:

            # CUse function to check if the word exists
            is_word_valid = True

            if is_word_valid:

                # Get the synonyms
                synonyms = [
                    "little",
                    "small-scale",
                    "compact",
                    "bijou",
                    "portable",
                    "tiny",
                    "miniature",
                    "mini",
                    "minute",
                    "micro",
                ]

                # Create embed
                embed = self.create_synonym_embed(word, synonyms)
                await ctx.send(embed=embed)

            else:
                await ctx.send(f"Sorry, couldn't find any synonyms for `{word}`.")

        else:
            await ctx.send("Sorry, couldn't find any synonyms.")

    @commands.guild_only()
    @dictionary.command(
        name="antonym",
        aliases=["ant"],
        brief="Provides a list of antonyms for the word given.",
        help="Provides a list of antonyms for the word given. This is done in english by default.",
    )
    async def dictionary_antonym(self, ctx, word=None):
        """ Provides a list of antonyms for the word given. 
        
        This is done in english by default. 
        """
        if word is not None:

            # Use function to check if the word exists
            is_word_valid = True

            if is_word_valid:

                # Get the antonyms
                antonyms = [
                    "big",
                    "large",
                    "heavily built",
                    "tall",
                    "generous",
                    "ample",
                    "major",
                    "substantial",
                ]

                # Create embed
                embed = self.create_antonym_embed(word, antonyms)
                await ctx.send(embed=embed)

            else:
                await ctx.send(f"Sorry, couldn't find any antonyms for `{word}`")

        else:
            await ctx.send("Sorry, couldn't find any antonyms.")

    @commands.guild_only()
    @dictionary.command(
        name="similar",
        aliases=["sim"],
        brief="Provides a list of words that have similar sound or spelling as the given word. (homonyms/homographs)",
        help="Provides a list of words that have similar sound or spelling as the given word (homonyms/homographs). This is done in english by default.",
    )
    async def dictionary_similar(self, ctx, word=None):
        """ Provides a list of words that have similar sound or spelling as the given word (homonyms/homographs).


        This is done in english by default.
        """
        if word is not None:

            # Use function to check if the word exists
            is_word_valid = True

            # Use function to check if the word has homographs (similar spelling words)
            word_has_similar = True

            if not is_word_valid or not word_has_similar:
                await ctx.send(
                    f"Sorry, couldn't find similar sounds or spelling words for `{word}`."
                )

            else:
                # Get the homonyms/homographs (similar sound words/similar spelling words)
                similar = [
                    {
                        "word": "bass",
                        "definition": "any of numerous edible marine or freshwater bony fishes.",
                    },
                    {"word": "bass", "definition": "deep or grave in tone."},
                    {"word": "bass", "definition": "a coarse tough fiber from palms."},
                ]

                # Create similar spelling embed
                embed = self.create_similar_embed(word, similar)
                await ctx.send(embed=embed)

        else:
            await ctx.send("Sorry, couldn't find similar spelling words.")

    @commands.guild_only()
    @dictionary.command(
        name="rhyme",
        brief="Provides a list of words that rhyme.",
        help="Provides a list of words that rhyme with the given word. This is done in english by default.",
    )
    async def dictionary_rhyme(self, ctx, word=None):
        """ Provides a list of words that rhyme with the given word. 

        This is done in english by default. 
        """
        if word is not None:

            # Use function to check if the word exists
            is_word_valid = True

            # Use function to check if the word has rhymes
            word_has_rhyme = True

            if not is_word_valid or not word_has_rhyme:
                await ctx.send(f"Sorry, couldn't find rhymes for `{word}`.")

            else:
                # Get the rhymes
                rhymes = [
                    "santa",
                    "anna",
                    "piano",
                    "Indiana",
                    "Montana",
                    "Hannah",
                    "nana",
                    "americana",
                    "bandanna",
                    "cabana",
                ]

                # Create similar spelling embed
                embed = self.create_rhyme_embed(word, rhymes)
                await ctx.send(embed=embed)

        else:
            await ctx.send("Sorry, couldn't find similar spelling words.")

    @commands.guild_only()
    @dictionary.command(
        name="wotd",
        brief="Programs a quote of the day for the specified channels.",
        help="Programs a quote of the day for the specified channels. This is done in english by default.",
    )
    async def dictionary_wotd(
        self,
        ctx,
        status=None,
        language="english",
        time=None,
        channels: commands.Greedy[discord.TextChannel] = "server",
    ):
        """ Programs a quote of the day for the specified channels. 

        This is done in english by default.
        """
        if status is not None and time is not None:
            # Use function to check to validate time string passed. This can be implemented as a converter
            is_time_valid = True

            # Use function to check if the language is valid
            is_language_valid = True

            if status.lower() != "enable" and status.lower() != "disable":
                await ctx.send("Sorry, wrong status given.")

            elif not is_language_valid:
                await ctx.send("Sorry, language is not valid.")

            elif not is_time_valid:
                await ctx.send("Sorry, wrong time format given.")

            else:
                # If no channels are specified
                if channels != "server":
                    programmed_channels = ", ".join(
                        ["`#" + channel.name + "`" for channel in channels]
                    )

                # Setup the word of the day for all channels
                else:
                    # Get all the channels from the server
                    channels = ctx.guild.channels
                    programmed_channels = "All channels"

                # Format everything
                status = status.lower().capitalize()
                language = language.lower().capitalize()

                embed = self.create_word_of_the_day_embed(
                    status, programmed_channels, time, language
                )
                await ctx.send(embed=embed)

        else:
            await ctx.send("Couldn't setup word of the day.")

    @commands.guild_only()
    @dictionary.command(
        name="random-word",
        aliases=["rand-wrd"],
        brief="Shows a random word with its definition",
        help="Shows a random word with its definition. This is done in english by default.",
    )
    async def dictionary_random_word(self, ctx):
        """ Shows a random word with its definition. 

        This is done in english by default. 
        """
        # Get a random word and its definition from the database
        word = "bot"
        definition = "An autonomous program on a network (especially the Internet) that can interact with computer systems or users, especially one designed to respond or behave like a player in an adventure game."

        # Create embed from random word and definition
        embed = self.create_definition_embed(word, definition)

        await ctx.send(embed=embed)

    @commands.guild_only()
    @dictionary.group(
        name="status",
        brief="Shows the word of the day status of the server.",
        help="Shows the word of the day status of the server.",
        invoke_without_commands=True,
    )
    async def dictionary_status(self, ctx):
        server = ctx.guild.name
        await ctx.send(f"Word of the Day status for server `{server}`")

    @commands.guild_only()
    @dictionary_status.command(
        name="channels",
        brief="Shows the word of the day status of the channels specified.",
        help="Shows the word of the day status of the channels specified.",
    )
    async def dictionary_status_channels(
        self, ctx, channels: commands.Greedy[discord.TextChannel] = None
    ):
        if channels is not None:
            channel_str = ", ".join(["`#" + channel.name + "`" for channel in channels])
            # Query the channels in the database
            await ctx.send(f"Word of the Day status for {channel_str}.")
        else:
            await ctx.send(f"Couldn't get Word of the Day status.")


def setup(bot):
    """ Setups up the dictionary cog for the bot. """
    logger.info("Loading Dictionary Cog")
    bot.add_cog(DictionaryCog(bot))


def teardown(bot):
    """ Tears down the dictionary cog for the bot. """
    logger.info("Unloading Dictionary Cog")
    bot.remove_cog("cogs.dictionary_cog")
