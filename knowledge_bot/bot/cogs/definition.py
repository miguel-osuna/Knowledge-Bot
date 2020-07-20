from discord.ext import commands, tasks


class Definition(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.printer.start()

    # Events
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author != self.bot.user:
            await message.channel.send("This is from definition")

    # Tasks
    @tasks.loop(seconds=10.0)
    async def printer(self):
        print("This is a loooped task in definition")

    # Commands
    @commands.command(name="definition", help="Looks for the definition of a word")
    async def text_definition(
        self, ctx, word: str, word_language="english", definition_language="english"
    ):
        if word:
            await ctx.send("This is your definition.")


def setup(bot):
    bot.add_cog(Definition(bot))
