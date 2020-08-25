import discord
from discord.ext import commands

import asyncio

from cogs.utils.deleteMessage import deleteMessage
from cogs.utils.prettyList import prettyList


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name="exec", hidden=True)
    async def _exec(self, context, *, code):
        """execute code sent from discord CAN BREAK THE BOT"""
        code = code.strip("`")

        global bot, ctx
        bot = self.bot
        ctx = context

        exec(
            "async def __ex():\n global bot\n global ctx\n " + 
                "\n ".join(code.split("\n"))
        )

        await locals()['__ex']()

    @commands.is_owner()
    @commands.command(hidden=True)
    async def servers(self, ctx):
        title = f"Running on {len(self.bot.guilds)} servers"
        guilds = [
            f"{g.name} member_count: {g.member_count}" for g in self.bot.guilds]

        await prettyList(ctx, title, guilds, maxLength=0)

    @commands.is_owner()
    @commands.command(hidden=True)
    async def thonk(self, ctx):
        """thonk emoji"""
        await deleteMessage(ctx)
        await ctx.send("<:thinking1:710563810582200350><:thinking2:710563810804498452>\n<:thinking3:710563823819554816><:thinking4:710563824079732756>")


def setup(bot: commands.Bot):
    bot.add_cog(Owner(bot))
