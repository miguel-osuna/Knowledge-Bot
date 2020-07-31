# Third party imports
from discord.ext import commands, tasks

# Local applications
from util.logger import generate_logger

logger = generate_logger(__name__)


class OwnerCog(commands.Cog):
    def __init__(self, bot):
        """ Initilialisation for OwnerCog instance. """
        self.bot = bot

    # Commands
    @commands.is_owner()
    @commands.command(name="load", help="Loads a specified extension/cog", hidden=True)
    async def load_cog(self, ctx, *, cog: str):
        """ Command which loads a module. """
        try:
            self.bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send(f"**`SUCCESS`**")

    @commands.is_owner()
    @commands.command(
        name="unload", help="Unloads a specified extension/cog", hidden=True
    )
    async def unload_cog(self, ctx, *, cog: str):
        """ Command which unloads a module. """
        try:
            self.bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send(f"**`SUCCESS:`**")

    @commands.is_owner()
    @comands.command(
        name="reload", help="Reloads a specific extension/cog", hidden=True
    )
    async def reload_cog(self, ctx, *, cog: str):
        """ Command which reloads a module. """
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            self.bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send(f"**`SUCCESS:`**")


def setup(bot):
    bot.add_cog(OwnerCog(bot))
