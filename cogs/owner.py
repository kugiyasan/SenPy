import discord
from discord.ext import commands

import asyncio


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(hidden=True)
    async def eval(self, ctx, *, code):
        """evaluate code sent from discord CAN BREAK THE BOT"""
        try:
            await ctx.send(f"```{eval(code.strip('`'))}```")
        except Exception as err:
                await ctx.send(f"```{err}```")

    @commands.is_owner()
    @commands.command(hidden=True)
    async def exec(self, ctx, *, code):
        """execute code sent from discord CAN BREAK THE BOT"""
        try:
            await ctx.send(f"```{exec(code.strip('`'))}```")
        except Exception as err:
                await ctx.send(f"```{err}```")

    @commands.is_owner()
    @commands.command(hidden=True)
    async def starteval(self, ctx):
        """execute multiple lines of code"""
        await ctx.send("```Waiting for code...```")

        def check(m):
            return (m.author == ctx.author
                    and m.channel == ctx.channel)

        while True:
            try:
                res = await self.bot.wait_for("message", check=check, timeout=300)
            except asyncio.exceptions.TimeoutError:
                await ctx.send("```Exiting...```")
                return

            if res.content == "stop":
                await ctx.send("```Exiting...```")
                return

            try:
                await ctx.send(f"```{eval(res.content.strip('`'))}```")
            except Exception as err:
                await ctx.send(f"```{err}```")


def setup(bot: commands.Bot):
    bot.add_cog(Owner(bot))
