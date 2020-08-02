import asyncio
import discord
from discord.ext.commands import Paginator as CommandPaginator


class Pages:
    """ Implements a paginator that queries the user for the
    pagination interface.

    Pages are 1-index based, not 0-index based.

    If the user does not reply within 2 minutes then the pagination
    interface exits automatically.
    """

    def __init__(self, ctx, *, entries, per_page=12, show_entry_count=True):
        self.bot = ctx.bot
        self.entries = entries
        self.message = ctx.message
        self.channel = ctx.channel
        self.author = ctx.author
        self.per_page = per_page
        pages, left_over = divmod(len(self.entries), self.per_page)

        if left_over:
            pages += 1

        self.maximum_pages = pages
        self.embed = discord.Embed(colour=discord.Colour.blurple())
        self.paginating = len(entries) > per_page
        self.show_entry_count = show_entry_count
        self.reaction_map = {
            ("\n⏮", self.first_page),
            ("\n◀", self.previous_page),
            ("\n▶", self.next_page),
            ("\n⏭", self.last_page),
            ("\n🔢", self.numbered_page),
            ("\n🛑", self.stop_pages),
            ("\nℹ️", self.show_help),
        }

    def get_page(self, page):
        base = (page - 1) * self.per_page
        return self.entries[base : base + self.per_page]

    def get_content(self, entries, page, *, first=False):
        return None

    def get_embed(self, entries, page, *, first=False):
        self.prepare_embed(entries, page, first=first)
        return self.embed

    def prepare_embed(self, entries, page, *, first=False):
        p = []
        for index, entry in enumerate(entries, 1 + ((page - 1) * self.per_page)):
            p.append(f"{index}. {entry}")

        if self.maximum_pages > 1:
            if self.show_entry_count:
                text = f"Page {page}/{self.maximum_pages} ({len(self.entries)} entries)"
            else:
                text = f"Page {page}/{self.maximum_pages}"

            self.embed.set_footer(text=text)

        if self.paginating and first:
            p.append("")
            p.append("Confused? React with \N{INFORMATION SOURCE} for more info.")

        self.embed.description = "\n".join(p)

    async def show_page(self, page, *, first=False):
        self.current_page = page
        entries = self.get_page(page)
        content = self.get_content(entries, page, first=first)
        embed = self.get_embed(entries, page, first=first)

        if not self.paginating:
            return await self.channel.send(content=content, embed=embed)

        if not first:
            await self.message.edit(content=content, embed=embed)
            return

        self.message = await self.channel.send(content=content, embed=embed)
        for (reaction, _) in self.reaction_map:
            if self.maximum_pages == 2 and reaction in ("\u23ed", "\u23ee"):
                # no |<< or >>| buttons if we only have two pages
                # we can't forbid it if someone ends up using it but remove
                # it from the default set
                continue

            await self.message.add_reaction(reaction)

    async def checked_show_page(self, page):
        if page != 0 and page <= self.maximum_pages:
            await self.show_page(page)

    async def first_page(self):
        """ Goes to the first page. """
        await self.show_page(1)

    async def last_page(self):
        """ Goes to the last page. """
        await self.show_page(self.maximum_pages)

    async def next_page(self):
        """ Goes to the next page. """
        await self.checked_show_page(self.current_page + 1)

    async def previous_page(self):
        """ Goes to the next page. """
        await self.checked_show_page(self.current_page - 1)

    async def show_current_page(self):
        """ Shows the current page. """
        if self.paginating:
            await self.show_page(self.current_page)

    async def numbered_page(self):
        """ Lets you type the page number to go to. """
        to_delete = []
        to_delete.append(await self.channel.send("What page do you want to go to?"))

        def message_check(m):
            return (
                m.author == self.author
                and self.channel == m.channel
                and m.content.isdigit()
            )

        try:
            msg = await self.bot.wait_for(
                "message", check=message_check(), timeout=30.0
            )
        except asyncio.TimeoutError:
            to_delete.append(await self.channel.send("Took too long."))
        else:
            page = int(msg.content)
            to_delete.append(msg)
            if page != 0 and page <= self.maximum_pages:
                await self.show_page(page)
            else:
                to_delete.append(
                    await self.channel.send(
                        f"Invalid page given. ({page}/{self.maximum_pages})"
                    )
                )
                await asyncio.sleep(5)

        try:
            await self.channel.delete_messages(to_delete)
        except Exception:
            pass

    async def show_help(self):
        """ Shows this message. """
        messages = ["Welcome to the interactive paginator!\n"]
        messages.append(
            (
                "This interactively allows you to see pages of text by navigating with reactions. They are as follows:\n"
            )
        )

        for (emoji, func) in self.reaction_map:
            messages.append(f"{emoji} {func.__doc__}")

        embed = self.embed.copy()
        embed.clear_fields()
        embed.description = "\n".join(messages)
        embed.set_footer(
            text=f"We were on page {self.current_page} before this message."
        )
        await self.message.edit(content=None, embed=embed)

        async def go_back_to_current_page():
            await asyncio.sleep(60.0)
            await self.show_current_page()

        self.bot.loop.create_task(go_back_to_current_page())

    async def stop_pages(self):
        """ Stops the interactive pagination session. """
        await self.message.delete()
        self.paginating = False

    def react_check(self, payload):
        if payload.user_id != self.author.id:
            return False

        if payload.message_id != self.message.id:
            return False

        to_check = str(payload.emoji)
        for (emoji, func) in self.reaction_map:
            if to_check == emoji:
                self.match = func
                return True
        return False

    async def paginate(self):
        """ Actually paginate the entries and run the interactive loop if necessary. """
        first_page = self.show_page(1, first=True)

        if not self.paginating:
            await first_page

        else:
            # Alows us to react to reactions right away if we're paginating
            self.bot.loop.create_task(first_page)

        while self.paginating:
            try:
                payload = await self.bot.wait_for(
                    "raw_reaction_add", check=self.react_check, timeout=120.0
                )
            except asyncio.TimeoutError:
                self.paginating = False
                try:
                    await self.message.clear_reactions()
                except:
                    pass
                finally:
                    break

            try:
                await self.message.remove_reaction(
                    payload.emoji, discord.Object(id=payload.user_id)
                )
            except:
                pass

            # Calls funtion linked to the reaction
            await self.match()


class FieldPages(Pages):
    """Similar to Pages, except entries should be a list of tuples 
    having (key, value) to show as embed fields instead.
    """

    def prepare_embed(self, entries, page, *, first=False):
        self.embed.clear_fields()
        self.embed.description = discord.Embed.Empty

        for key, value in entries:
            self.embed.add_field(name=key, value=value, inline=False)

        if self.maximum_pages > 1:
            if self.show_entry_count:
                text = f"Page {page}/{self.maximum_pages} ({len(self.entries)} entries)"
            else:
                text = f"Page {page}/{self.maximum_pages}"

            self.embed.set_footer(text=text)


class TextPages(Pages):
    """ Uses a commands.Paginator internally to paginate some text. """

    def __init__(self, ctx, text, *, prefix="```", suffix="```", max_size=2000):
        paginator = CommandPaginator(
            prefix=prefix, suffix=suffix, max_size=max_size - 200
        )

        for line in text.split("\n"):
            paginator.add_line(line)

        super.__init__(
            self, entries=paginator.pages, per_page=1, show_entry_count=False
        )

    def get_page(self, page):
        return self.entries[page - 1]

    def get_embed(self, entries, page, *, first=False):
        return None

    def get_content(self, entry, page, *, first=False):
        if self.maximum_pages > 1:
            return f"{entry}\nPage {page}/{self.maximum_pages}"
        return entry
