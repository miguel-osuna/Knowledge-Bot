from discord.ext import commands, tasks


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.printer.start()

    # Events
    @commands.Cog.listener()
    async def on_message(self, message):
        """ Called when a message is sent """

        if message.author != self.bot.user:
            await message.channel.send("This is from settings")

    # Tasks
    @tasks.loop(seconds=10.0)
    async def printer(self):
        print("This is a looped task in settings")

    # Commands
    @commands.command(name="settings", help="Configure Knowledge Bot in your server.")
    async def settings(self, ctx):
        await ctx.send("Your settings have changed.")


def setup(bot):
    bot.add_cog(Settings(bot))
