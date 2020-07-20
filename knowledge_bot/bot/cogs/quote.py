from discord.ext import commands, tasks


class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.printer.start()

    # Events
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author != self.bot.user:
            await message.channel.send("This is from quote")

    # Tasks
    @tasks.loop(seconds=10.0)
    async def printer(self):
        print("This is a loooped task in quote")

    # Commands
    @commands.command(name="quote", help="Generate a quote.")
    async def generate_quote(
        self, ctx, category=None, author=None, type="random", language="english"
    ):
        await ctx.send("You know nothing, John Snow")


def setup(bot):
    bot.add_cog(Quote(bot))
