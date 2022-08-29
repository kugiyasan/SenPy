import discord
from discord.ext import commands

import os
from typing import Tuple

# from .utils.dbms import db
from .utils.get_extensions import get_extensions


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name="eval", hidden=True)
    async def _eval(self, context, *, code):
        """Similar to the exec command, except that it sends back the result"""
        global bot, ctx
        bot = self.bot
        ctx = context

        code = f"async def __ex():\n  global bot, ctx\n  await ctx.send({code})"

        print(code)
        exec(code)

        await locals()["__ex"]()
        await context.message.add_reaction("✅")

    @commands.is_owner()
    @commands.command(name="exec", hidden=True)
    async def _exec(self, context, *, code):
        """Execute code sent from discord CAN BREAK THE BOT"""
        global bot, ctx
        bot = self.bot
        ctx = context

        code = code.strip("`")
        code = "async def __ex():\n  global bot, ctx\n  " + "\n  ".join(
            code.split("\n")
        )

        print(code)
        exec(code)

        await locals()["__ex"]()
        await context.message.add_reaction("✅")

    @commands.is_owner()
    @commands.command(aliases=["sh"], hidden=True)
    async def shell(self, ctx: commands.Context, *, command: str):
        """Execute a shell command and send back the output"""
        stream = os.popen(command)
        output = stream.read()
        await ctx.send(f"```{output}```")

    # @commands.is_owner()
    # @commands.command(hidden=True)
    # async def sql(self, ctx: commands.Context, code: str, *values: Tuple[str]):
    #     """Send a query to the database"""
    #     code = code.strip("`").lower()

    #     if code.startswith("select"):
    #         data = db.get_data(code, values)
    #         await ctx.send(data)
    #     else:
    #         db.set_data(code, values)
    #         await ctx.message.add_reaction("✅")

    @commands.is_owner()
    @commands.command(hidden=True)
    async def activity(self, ctx: commands.Context, *, string: str):
        """Change the activity status of the bot"""
        occupation = discord.Game(name=string)
        await self.bot.change_presence(activity=occupation)
        await ctx.message.add_reaction("✅")

    @commands.is_owner()
    @commands.command(hidden=True, aliases=["rl"])
    async def reload(self, ctx: commands.Context):
        """Reloads the bot extensions without rebooting the entire program"""
        try:
            for ext in get_extensions():
                try:
                    await self.bot.reload_extension(ext)
                except commands.errors.ExtensionNotLoaded:
                    await self.bot.load_extension(ext)
        except commands.ExtensionFailed:
            await ctx.send("Reloading failed")
            raise

        await ctx.message.add_reaction("✅")
        print("\033[94mReloading successfully finished!\033[0m\n")


async def setup(bot: commands.Bot):
    await bot.add_cog(Owner(bot))
