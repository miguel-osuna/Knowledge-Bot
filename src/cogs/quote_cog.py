# Standard library imports
import typing
import pdb
import pytz
from datetime import datetime

# Third party imports
import discord
from discord.ext import commands, tasks

# Local applications
from util.logger import generate_logger
from paginator import Pages

logger = generate_logger(__name__)


class QuotePaginator(Pages):
    """ Quote of the Day Status Paginator. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class QuoteCog(commands.Cog, name="Quote"):
    def __init__(self, bot):
        self.bot = bot
        self.printer.start()
        self.single_quotes_sent = []
        self.multiple_quotes_sent = []

    def create_category_list_embed(self, categories):
        """ Creates an embed to show the categories available and their quotes. """
        category_names = ""
        category_totals = ""

        for category in categories:
            category_names += "{}\n".format(category["name"])
            category_totals += "*{}*\n".format(category["total"])

        embed = discord.Embed(title="Quote Categories", colour=discord.Colour.blue())
        embed.add_field(name="Category", value=category_names)
        embed.add_field(name="Quotes", value=category_totals)

        # Add timestamp to the embed
        embed.timestamp = datetime.utcnow()

        return embed

    def create_quote_embed(self, quote, author, category, author_picture_url, channel):
        """ Creates an embed to show a quote. """
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.description = f"```📜 {quote}```"
        embed.set_thumbnail(url=author_picture_url)
        embed.add_field(name="Author", value=f"— *{author}*", inline=True)
        embed.add_field(name="Category", value=f"{category}", inline=True)

        if not isinstance(channel, discord.DMChannel):
            embed.set_footer(text="React with ❤️ to forward this quote to your inbox")

        # Add timestamp to the embed
        embed.timestamp = datetime.utcnow()
        return embed

    def create_quote_list_embed(self, author_quote_list, channel):
        """ Creates an embed to show a list of quotes. """

        embed = discord.Embed(colour=discord.Colour.blue())

        for author_dict in author_quote_list:
            quote_entries = ""
            author_name = author_dict["name"]

            for author_quote in author_dict["quote_list"]:
                quote_entries += "📜 {} ({})\n\n".format(
                    author_quote["quote"], author_quote["category"]
                )

            # Add author and its quotes
            embed.add_field(
                name=f"*{author_name}*", value=f"```{quote_entries}```", inline=False,
            )

        if not isinstance(channel, discord.DMChannel):
            embed.set_footer(text="React with ❤️ to forward this quote to your inbox.")

        # Add timestamp to the embed
        embed.timestamp = datetime.utcnow()

        return embed

    def create_quote_detection_embed(self, quote, author, author_picture):
        """ Creates an embed to tell the user if a quote is found. """
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.title = f"Quote from *{author}*"
        embed.description = f"```{quote}```"
        embed.set_thumbnail(url=author_picture)
        embed.timestamp = datetime.utcnow()

        return embed

    def create_quote_of_the_day_embed(
        self, status, channels, time, language, author, category
    ):
        """ Creates an embed to notice the user when a quote is programmed. """
        embed = discord.Embed(
            title="Quote of the Day Setup", colour=discord.Colour.blue()
        )

        embed.add_field(name="❓ Status", value=f"{status}\u200B\n", inline=True)
        embed.add_field(name="💬 Channels", value=f"{channels}\u200B\n", inline=True)
        embed.add_field(name="⌚ Time", value=f"{time}\u200B", inline=True)
        embed.add_field(name="🌎 Language", value=f"{language}\u200B", inline=True)
        embed.add_field(name=" ✍️ Author", value=f"{author}\u200B", inline=True)
        embed.add_field(name="📋 Category", value=f"{category}\u200B", inline=True)
        embed.timestamp = datetime.utcnow()

        return embed

    def create_quote_status_embed(self, qotd_config_list):
        """ Creates a paginator embed to show the quote of the day status. """
        embed = discord.Embed(
            title="Quote of the Day Status", colour=discord.Colour.blue()
        )

        return embed

    # Event Listeners
    @commands.Cog.listener()
    async def on_message(self, message):
        """ Called when a message is sent 
        
        May be not necessary (?)
        """

        if message.author != self.bot.user:
            # await message.channel.send("This is from quote")
            pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """ Called when a message is edited 
        
        May not be necessary (?)
        """

        prev_message = before
        next_message = after

        if (
            prev_message.author != self.bot.user
            and next_message.author != self.bot.user
        ):
            # await next_message.channel.send("This is from quote")
            pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """ Called when a message has a reaction added to it 
        
        When a user reacts to a quote embedded by the bot with the proper reactions,
        it can be sent to him by using DM or it can be saved to their list of personal quotes, 
        it all depends on the reaction used. 
        """
        # await reaction.channel.send("This is from quote")

        # Check that the reaction channels is not done on a private channel and the user is not a bot
        if not isinstance(reaction.message.channel, discord.DMChannel) and not user.bot:

            if reaction.emoji == "❤️":
                # Get the ID from the message that was reacted to
                message_id = reaction.message.id
                message_embed = reaction.message.embeds[0]

                # Remove the footer from the embed to send it to the user
                message_embed.set_footer(text=discord.Embed.Empty)

                # Check if the message that was reacted is a quote embed message
                for quote_message in self.single_quotes_sent:
                    if message_id == quote_message.id:
                        # Create a DM channel with the user to send the embed
                        await user.create_dm()
                        await user.dm_channel.send(embed=message_embed)

                # Now check for the multiple quote embed messages
                for quote_message in self.multiple_quotes_sent:
                    if message_id == quote_message.id:
                        # Create a DM channel with the user to send the embed
                        await user.create_dm()
                        await user.dm_channel.send(embed=message_embed)

    @commands.Cog.listener()
    async def on_private_channel_delete(self, channel):
        """ Called whenever a private channel is deleted 
        
        If a private channel is deleted that had any configuration related to the quote 
        functionality, make sure to also remove it. 
        """
        pass

    @commands.Cog.listener()
    async def on_private_channel_update(self, before, after):
        """ Called whenever a private group DM is updated. e.g. changed name or topic 
        
        Ifa private channel is updated that had any configuration related to the quote
        functionality, make sure to also update it with the newest channel values. 
        """
        pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """ Callend when a Member leaves a Guild 
        
        If the member that left the Guild had any quotes saved, also delete them from the database. 
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

        If the member updates their values, make sure to also update that information
        in the database.       
        """
        pass

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        """ Called when a User updates their profile 
        
        This is called when one or more of the following things change:
        - avatar 
        - username
        - discriminator

        If the user user updates its information, make sure to also update that information
        in the database (?)
        """
        pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """ Callend when a Guild is removed from the Client 
        
        If the Guild is removed, make sure to also remove any stored data.
        """
        pass

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        """ Called when a Guild updates 
        
        If the Guild is updated, make sure to also update the database with the newer values
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
        # logger.warning("This is a warning from quote_cog")
        pass

    # Commands
    @commands.group(name="quote", aliases=["qt"], help="Commands for quote generation.")
    async def quote(self, ctx):
        """Commands for quote generation. Use `~help quote` to view subcommands."""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"Incorrect usage. Use `{ctx.prefix}help quote` for help.")
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

    @quote.command(
        name="list",
        aliases=["ls"],
        brief="Sends list of all categories and authors available.",
        help="Sends list of all categories and authors available.",
    )
    async def quote_list(self, ctx):
        # Query all the categories from the database
        # Query all the authors from the database

        categories = [
            {"name": "Love", "total": 100},
            {"name": "Friendship", "total": 200},
            {"name": "History", "total": 300},
        ]
        embed = self.create_category_list_embed(categories)

        await ctx.author.send(embed=embed)

    @quote.group(
        name="generate",
        aliases=["genr"],
        brief="Embeds message with a random quote in the text channel.",
        help="Embeds message with a random quote in the text channel.",
        invoke_without_command=True,
    )
    async def quote_generate(
        self, ctx, language="en", *, category_or_author: str = None,
    ):
        if category_or_author is not None:
            # Check if the quote and authors are in the database
            category_or_author_in_database = True

            if category_or_author_in_database:

                # Get random quote from the database according to the author or category
                # Mock quote
                random_quote = {
                    "quote": "Courage is resistance to fear, mastery of fear - not absence of fear.",
                    "author": "Mark Twain",
                    "author_picture_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Mark_Twain_by_AF_Bradley.jpg/220px-Mark_Twain_by_AF_Bradley.jpg",
                    "category": "Love",
                }

                embed = self.create_quote_embed(
                    quote=random_quote["quote"],
                    category=random_quote["category"],
                    author=random_quote["author"],
                    author_picture_url=random_quote["author_picture_url"],
                    channel=ctx.channel,
                )

                # Retrieve the message that was sent to the channels
                message = await ctx.channel.send(embed=embed)

                # If the quote generate command was not sent by DM, add an emoji to the message
                if not isinstance(ctx.channel, discord.DMChannel):
                    await message.add_reaction("❤️")

                    # To keep track of the message and its reactions,
                    # add it to a list of single quotes sent.

                    # Could also add it to the database to keep track
                    # of different guild quotes.
                    self.single_quotes_sent.append(message)

            else:
                await ctx.send("Couldn't find author or quote.")

        else:
            await ctx.send("Couldn't generate quote.")

    @quote_generate.command(
        name="list",
        aliases=["ls"],
        brief="Embeds message with a list of quotes in the text channel.",
        help="Embeds message with a list of quotes in the text channel",
    )
    async def quote_generate_list(
        self,
        ctx,
        language="en",
        quote_entries: typing.Optional[int] = 10,
        *,
        category_or_author: str = None,
    ):
        if category_or_author is not None:
            # Check if the category or author is in the database
            category_or_author_in_database = True

            if category_or_author_in_database:

                # Get `quote_entries` number of quotes from the database
                # Mock quotes

                author_quotes = [
                    {
                        "name": "Mark Twain",
                        "author_picture": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Mark_Twain_by_AF_Bradley.jpg/220px-Mark_Twain_by_AF_Bradley.jpg",
                        "quote_list": [
                            {
                                "quote": "Good friends, good books, and a sleepy conscience: this is the ideal life.",
                                "category": "Friendship",
                            },
                            {
                                "quote": "Whenever you find yourself on the side of the majority, it is time to reform (or pause and reflect).",
                                "category": "Wisdom",
                            },
                            {
                                "quote": "Never put off till tomorrow what may be done day after tomorrow just as well.",
                                "category": "Humor",
                            },
                        ],
                    },
                    {
                        "name": "Frank Zappa",
                        "author_picture": "https://images.gr-assets.com/authors/1315160559p2/22302.jpg",
                        "quote_list": [
                            {
                                "quote": "Without deviation from the norm, progress is not possible.",
                                "category": "Philosophy",
                            },
                            {
                                "quote": "So many books, so little time.",
                                "category": "Humor",
                            },
                        ],
                    },
                ]

                embed = self.create_quote_list_embed(
                    author_quote_list=author_quotes, channel=ctx.channel
                )

                # Retrieve the message that was sent to the channels
                message = await ctx.channel.send(embed=embed)

                # If the quote generate list command was not sent by DM, add an emoji to the message
                if not isinstance(ctx.channel, discord.DMChannel):
                    await message.add_reaction("❤️")

                    # To keep track of the message and its reactions,
                    # add it to a list of multple quotes sent.

                    # Could also add it to the database to keep track
                    # of different guild quotes.
                    self.multiple_quotes_sent.append(message)

            else:
                await ctx.send("Couldn't find author or quote.")

        else:
            await ctx.send("Couldn't generate quote.")

    @commands.guild_only()
    @quote.command(
        name="qotd",
        brief="Programs a quote of the day for the specified channels.",
        help="Programs a quote of the day for the specified channels. The default language for the quote is english.",
    )
    async def quote_qotd(
        self,
        ctx,
        status=None,
        language="english",
        time=None,
        channels: commands.Greedy[discord.TextChannel] = "server",
        category=None,
        *,
        author=None,
    ):
        if (
            status is not None
            and time is not None
            and category is not None
            and author is not None
        ):

            # Use function to validate time string passed. This can be implemented as a Converter
            is_time_valid = True

            # Use function to check if the language is valid
            is_language_valid = True

            # Use function to check if category is available in the database
            is_category_valid = True

            # Use function to check if author is available in the database
            is_author_valid = True

            if status.lower() != "enable" and status.lower() != "disable":
                await ctx.send("Sorry, wrong status given.")

            elif not is_language_valid:
                await ctx.send("Sorry, language is not valid.")

            elif not is_time_valid:
                await ctx.send("Sorry, wrong time format given.")

            elif not is_category_valid:
                await ctx.send("Sorry, the category is not available.")

            elif not is_author_valid:
                await ctx.send("Sorry, the author is not available.")

            else:
                # If no channels are specified
                if channels != "server":
                    programmed_channels = ", ".join(
                        ["`#" + channel.name + "`" for channel in channels]
                    )

                # Setup the quote of the day for all channels
                else:
                    # Get all the channels from the server
                    channels = ctx.guild.channels
                    programmed_channels = "All channels"

                # Format everything
                status = status.lower().capitalize()
                language = language.lower().capitalize()
                author = author.lower().title()
                category = category.lower().capitalize()

                embed = self.create_quote_of_the_day_embed(
                    status, programmed_channels, time, language, author, category,
                )
                await ctx.send(embed=embed)

        else:
            await ctx.send("Couldn't setup quote of the day.")

    @quote.command(
        name="detect",
        brief="Displays author and category of a given quote if it finds a match.",
        help="Displays author and category of a given quote if it finds a match.",
    )
    async def quote_detect(self, ctx, *, quote=None):
        if quote is not None:
            # Look for the quote in the database and retrieve its author and its category
            quote_found = True

            if quote_found:
                # Get the author and the author picture from the database
                quote = "Never put off till tomorrow what may be done day after tomorrow just as well."
                author = "Mark Twain"
                author_picture = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Mark_Twain_by_AF_Bradley.jpg/220px-Mark_Twain_by_AF_Bradley.jpg"

                embed = self.create_quote_detection_embed(quote, author, author_picture)
                await ctx.send(embed=embed)

            else:
                await ctx.send("Sorry, couldn't find an author for the quote.")

        else:
            # Notify couldn't detect the quote
            await ctx.send("Couldn't detect the quote.")

    @commands.guild_only()
    @quote.group(
        name="status",
        brief="Shows the quote status of the server.",
        help="Shows the quote status of the server.",
        invoke_without_commands=True,
    )
    async def quote_status(self, ctx):
        server = ctx.guild.name
        await ctx.send(f"Quote of the Day status for server `{server}`")

    @commands.guild_only()
    @quote_status.command(
        name="channels",
        brief="Shows the quote status of the channels specified.",
        help="Shows the quote status of the channels specified.",
    )
    async def quote_status_channels(
        self, ctx, channels: commands.Greedy[discord.TextChannel] = None
    ):
        if channels is not None:
            channel_str = ", ".join(["`#" + channel.name + "`" for channel in channels])
            # Query the channels in the database
            await ctx.send(f"Quote of the Day status for {channel_str}.")
        else:
            await ctx.send(f"Couldn't get status.")


def setup(bot):
    """ Sets up the quote cog for the bot. """
    logger.info("Loading Quote Cog")
    bot.add_cog(QuoteCog(bot))


def teardown(bot):
    """ Tears down the quote cog for the bot. """
    logger.info("Unloading Quote Cog")
    bot.remove_cog("cogs.quote_cog")
