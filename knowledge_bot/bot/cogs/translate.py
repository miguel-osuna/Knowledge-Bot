from discord.ext import commands, tasks


class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.printer.start()

    # Events
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author != self.bot.user:
            await message.channel.send("This is from translate")

    # Tasks
    @tasks.loop(seconds=10.0)
    async def printer(self):
        print("This is a loooped task in translate")

    # Commands
    channel_default_language = "english"

    @commands.command(name="translate", help="Translate a word or phrase.")
    async def translate_text(
        self,
        ctx,
        from_language=channel_default_language,
        to_language=None,
        *,
        text=None
    ):

        if to_language != None and text != None:
            await ctx.send("Text translated.")

        else:
            await ctx.send("Couldn't translate language.")


def setup(bot):
    bot.add_cog(Translate(bot))
