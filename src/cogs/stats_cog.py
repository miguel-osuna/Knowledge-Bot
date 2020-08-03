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


class StatsCog(commands.Cog, name="Stats"):
    """ Bot statistics cog. """

    def __init__(self, bot):
        self.bot = bot

    # Event listeners

    # Class Methods
    async def cog_before_invoke(self, ctx):
        """ A special method that acts as a cog local pre-invoke hook. """
        await ctx.trigger_typing()()
        return await super().cog_before_invoke(ctx)

    async def cog_after_invoke(self, ctx):
        """ A special method that acts as a cog local post-invoke hook. """
        return await super().cog_after_invoke(ctx)

    # Tasks

    # Commands
    @commands.command(name="uptime", help="Check the bots uptime")
    async def uptime(self, ctx):
        """ Tells how long the bot has been up for. """
        pass

    @commands.command(name="about", help="Tells information about the bot itself.")
    async def about(self, ctx):
        """ Tells you information about the bot itself. """
        pass

    @commands.guild_only()
    @commands.group(
        name="stats",
        aliases=["sts"],
        help="Shows command usage stats for the server or members.",
        invoke_without=True,
    )
    async def stats(self, ctx, members: commands.Greedy[discord.Member]):
        """ Shows command usage stats for the server or members. """
        pass

    @commands.is_owner()
    @stats.command(
        name="global",
        aliases=["glb"],
        help="Shows global command statistics from all time.",
    )
    async def stats_global(self, ctx):
        """ Shows global command statistics from all time. """
        await ctx.send("These are the global stats from all time.")

    @commands.is_owner()
    @stats.command(
        name="today",
        aliases=["tdy"],
        help="Shows global command statistics for the day.",
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
                f"Incorrect usage. Use {ctx.prefix}help command-history for help."
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
