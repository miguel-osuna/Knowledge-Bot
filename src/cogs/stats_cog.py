# Standard library imports
import typing
import json
import os
import pdb
import pytz
from os.path import dirname, abspath, join
from datetime import datetime
from math import floor

# Third party imports
import discord
from discord.ext import commands, tasks

# Local applications
from util.logger import generate_logger


BASE_PROJECT_PATH = dirname(dirname(dirname((abspath(__file__)))))
LANGUAGES_PATH = join(BASE_PROJECT_PATH, "data", "input", "langs.json")
VERSION = "v1.0"

logger = generate_logger(__name__)


class StatsCog(commands.Cog, name="Stats"):
    """ Bot statistics cog. """

    def __init__(self, bot):
        self.bot = bot

    def get_time_difference(self, start_datetime, end_datetime):
        delta = end_datetime - start_datetime
        months, remainder = divmod(delta.seconds, 60 * 60 * 24 * 30)
        days, remainder = divmod(remainder, 60 * 60 * 24)
        hours, remainder = divmod(remainder, 60 * 60)
        minutes, remainder = divmod(remainder, 60)
        seconds = remainder

        time_difference = "**{}** *months*, **{}** *days*, **{}** *hours*, **{}** *minutes*, **{}** *seconds*".format(
            months, days, hours, minutes, seconds
        )

        return time_difference

    def create_uptime_embed(self, start_datetime):
        """ Creates an embed to show the total uptime of the bot. """
        # Create the uptime string
        end_datetime = datetime.utcnow()
        uptime_string = self.get_time_difference(start_datetime, end_datetime)

        # Create uptime embed
        embed = discord.Embed(
            title="⏱️ Knowledge Bot Uptime", color=discord.Color.dark_magenta()
        )
        embed.description = f"\n\n{uptime_string}"
        embed.timestamp = end_datetime

        return embed

    def create_about_embed(
        self,
        server_invite_url,
        members,
        servers,
        channels,
        commands,
        version,
        start_datetime,
    ):
        """ Creates an embed to show information about the bot. """
        embed = discord.Embed(color=discord.Color.dark_magenta())
        embed.title = "🤖 Official Knowedge Bot Server Invite"
        embed.url = server_invite_url
        embed.description = "Knowledge Bot is a bot that offers you functionalities such as translation, dictionary, quote generation and more."

        end_datetime = datetime.utcnow()
        uptime_string = self.get_time_difference(start_datetime, end_datetime)
        uptime_string = uptime_string.replace(", ", "\n")

        # Create about embed
        embed.add_field(name="👥 Members", value=f"**{members}** in total", inline=True)
        embed.add_field(name="🖥️ Servers", value=f"**{servers}** in total", inline=True)
        embed.add_field(
            name="🌐 Channels", value=f"**{channels}** in total", inline=True
        )
        embed.add_field(name="❓ Status", value="Online", inline=True)
        embed.add_field(name="⏱️ Uptime", value=f"{uptime_string}", inline=True)
        embed.add_field(
            name="⚙️ Commands", value=f"**{commands}** in total", inline=True
        )

        embed.set_footer(text=f"Knowledge Bot {version}")
        embed.timestamp = end_datetime
        return embed

    def create_version_embed(self, version):
        """ Creates an embed to show the bots version. """
        embed = discord.Embed(color=discord.Color.dark_magenta())
        embed.title = f"Knowledge Bot `{version}`"
        embed.timestamp = datetime.utcnow()
        return embed

    def create_join_embed(self, version, bot_invite_url, server_invite_url):
        """ Creates an embed that includes a bot invitation to a server. """
        embed = discord.Embed(color=discord.Color.dark_magenta())
        embed.title = "🤖 Add Knowledge Bot to your Discord Server!"
        embed.description = "If you're interested in adding Knowledge Bot to your server, you'll find some links below to help you get started."
        embed.add_field(
            name="Knowledge Bot Invite", value=f"{bot_invite_url}", inline=False
        )
        embed.add_field(
            name="Knowledge Bot Support Server",
            value=f"{server_invite_url}",
            inline=False,
        )
        embed.set_footer(text=f"Knowledge Bot {version}")
        embed.timestamp = datetime.utcnow()
        return embed

    # Class Methods
    async def cog_before_invoke(self, ctx):
        """ A special method that acts as a cog local pre-invoke hook. """
        await ctx.trigger_typing()
        return await super().cog_before_invoke(ctx)

    async def cog_after_invoke(self, ctx):
        """ A special method that acts as a cog local post-invoke hook. """
        return await super().cog_after_invoke(ctx)

    # Commands
    @commands.command(name="uptime", help="Check the bots uptime")
    async def uptime(self, ctx):
        """ Tells how long the bot has been up for. """
        # Get the stating datetime variable from the bots database
        start_datetime = datetime(2020, 2, 10, 14, 40)

        embed = self.create_uptime_embed(start_datetime)
        await ctx.send(embed=embed)

    @commands.command(name="about", help="Tells information about the bot itself.")
    async def about(self, ctx):
        """ Tells you information about the bot itself. """
        # Embed variables
        version = VERSION
        start_datetime = datetime(2020, 2, 10, 14, 40)
        server_invite_url = "https://discord.gg/kCYHENR"
        total_members = len(self.bot.users)
        commands = len(self.bot.commands)
        guilds = 0
        text_channels = 0

        # Get every text channel from every guild the bot is in
        for guild in self.bot.guilds:
            guilds += 1
            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel):
                    text_channels += 1

        # Create embed
        embed = self.create_about_embed(
            server_invite_url,
            total_members,
            guilds,
            text_channels,
            commands,
            version,
            start_datetime,
        )
        await ctx.send(embed=embed)

    @commands.command(name="version", help="Tells the version of the bot.")
    async def version(self, ctx):
        """ Tells the version of the bot. """
        # Get bot version
        version = VERSION
        embed = self.create_version_embed(version)
        await ctx.send(embed=embed)

    @commands.command(
        name="join",
        aliases=["invite"],
        help="Sends a link to add Knowledge Bot to your server.",
    )
    async def join(self, ctx):
        """ Sends a link to add Knowledge Bot to your server. """
        version = VERSION
        bot_invite_url = "https://discord.com/api/oauth2/authorize?client_id=733908127497322517&permissions=8&scope=bot"
        server_invite_url = "https://discord.gg/kCYHENR"
        embed = self.create_join_embed(version, bot_invite_url, server_invite_url)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.group(
        name="stats",
        aliases=["sts"],
        help="Shows command usage stats for the server or members.",
        invoke_without=True,
    )
    async def stats(self, ctx, members: commands.Greedy[discord.Member] = "server"):
        """ Shows command usage stats for the server or members. """
        pass

    @commands.is_owner()
    @stats.command(
        name="global",
        aliases=["glb"],
        help="Shows global command statistics for all the servers from all time.",
    )
    async def stats_global(self, ctx):
        """ Shows global command statistics for all the servers from all time."""
        await ctx.send("These are the global stats from all time.")

    @commands.is_owner()
    @stats.command(
        name="today",
        aliases=["tdy"],
        help="Shows global command statistics for all the servers from the day.",
    )
    async def stats_today(self, ctx):
        """ Shows global command statistics for the day. """
        await ctx.send("These are the stats of today.")

    @commands.is_owner()
    @commands.command(
        name="bot-health", help="Bot health monitoring tools.", hidden=True
    )
    async def bothealth(self, ctx):
        """ Bot health monitoring tools. """
        pass

    @commands.is_owner()
    @commands.command(
        name="gateway", help="Provides gateway related statistics.", hidden=True
    )
    async def gateway(self, ctx):
        """ Gateway related statistics. """
        pass

    @commands.is_owner()
    @commands.command(
        name="debug-task", help="Debug a task by a memory location.", hidden=True
    )
    async def debug_task(self, ctx):
        """ Debug a task by a memory location. """
        pass

    @commands.is_owner()
    @commands.group(
        name="command-history",
        aliases=["cmd-hist"],
        help="Commands to check command history",
        hidden=True,
    )
    async def command_history(self, ctx):
        """ Commands to check command history. Use `~help command-history` to view subcommands"""

        if ctx.invoked_subcommand is None:
            await ctx.send(
                f"Incorrect usage. Use `{ctx.prefix}help command-history` for help."
            )
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

    @command_history.command(name="command", help="Show command history for a command.")
    async def command_history_command(
        self, ctx, days: typing.Optional[int] = 7, *, command: str
    ):
        """ Show command history for a command. """
        pass

    @command_history.command(name="guild", help="Show command historyh for a guild.")
    async def command_history_guild(
        self, ctx, days: typing.Optional[int] = 7, *, guild_id: int
    ):
        """ Show command history for a guild. """
        pass

    @command_history.command(name="user", help="Show command history for a user.")
    async def command_history_user(
        self, ctx, days: typing.Optional[int] = 7, *, user_id: int
    ):
        """ Show command history for a user. """
        pass

    @command_history.command(
        name="log", help="Show all command history log for N days.",
    )
    async def command_history_log(self, ctx, days: typing.Optional[int] = 7):
        """ Show all command history log for N days. """
        pass

    @command_history.command(name="cog", help="Show command history for a cog.")
    async def command_history_cog(self, ctx, days: typing.Optional[int] = 7):
        """ Show command history for a cog. """
        pass


def setup(bot):
    """ Sets up the translate cog for the bot. """
    bot.add_cog(StatsCog(bot))


def teardown(bot):
    """ Tears down the translate cog for the bot. """
    bot.remove_cog("stats_cog")
