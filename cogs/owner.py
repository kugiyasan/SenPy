import discord
from discord.ext import commands

import asyncio

from cogs.utils.deleteMessage import deleteMessage
from cogs.utils.prettyList import prettyList
from cogs.utils.dbms import conn, cursor


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name="exec", hidden=True)
    async def _exec(self, context, *, code):
        """execute code sent from discord CAN BREAK THE BOT"""
        global bot, ctx
        bot = self.bot
        ctx = context

        code = code.strip("`")
        code = "async def __ex():\n  global bot, ctx\n  " + \
            "\n  ".join(code.split("\n"))

        print(code)
        exec(code)

        await locals()["__ex"]()

    @commands.is_owner()
    @commands.command(hidden=True)
    async def sql(self, context, code, *values):
        global ctx, conn, cursor
        ctx = context
        conn = conn
        cursor = cursor

        code = code.strip("`").lower()
        wrappedCode = f"async def __ex():\n  global ctx, conn, cursor\n  with conn:\n    cursor.execute(\"\"\"{code}\"\"\", {values})"
        if code.startswith("select"):
            wrappedCode += "\n    await ctx.send(str(cursor.fetchall()))"

        print(wrappedCode)
        exec(wrappedCode)

        await locals()["__ex"]()

    @commands.is_owner()
    @commands.command(hidden=True)
    async def activity(self, ctx, *, string):
        occupation = discord.Activity(
            type=discord.ActivityType.playing, name=string)
        await self.bot.change_presence(activity=occupation)

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
