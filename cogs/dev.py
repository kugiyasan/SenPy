import discord
from discord.ext import commands
import asyncio


class Dev(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def test(self, ctx: commands.Context):
        file = discord.File("media/hanamaru.jpg", filename="image.png")
        embed = discord.Embed()
        embed.set_image(url="attachment://image.png")
        await ctx.send(file=file, embed=embed)

    @commands.command(hidden=True)
    async def e(self, ctx: commands.Context):
        page1 = discord.Embed(
            title="Page 1/3",
            description="Description",
            colour=discord.Colour.orange()
        )
        page2 = discord.Embed(
            title="Page 2/3",
            description="Description",
            colour=discord.Colour.gold()
        )
        page3 = discord.Embed(
            title="Page 3/3",
            description="Description",
            colour=discord.Colour.orange()
        )

        pages = [page1, page2, page3]

        message = await ctx.send(embed=page1)
        await message.add_reaction("\u23ee")
        await message.add_reaction("\u25c0")
        await message.add_reaction("\u25b6")
        await message.add_reaction("\u23ed")

        i = 0
        emoji = ""

        while True:
            if emoji == "\u23ee":
                i = 0
                await message.edit(embed=pages[i])
            if emoji == "\u25c0":
                if i > 0:
                    i -= 1
                    await message.edit(embed=pages[i])
            if emoji == "\u25b6":
                if i < 2:
                    i += 1
                    await message.edit(embed=pages[i])
            if emoji == "\u23ed":
                i = 2
                await message.edit(embed=pages[i])

            def check(reaction, member):
                return ctx.author == member

            try:
                res = await self.bot.wait_for("reaction_add", check=check, timeout=30)
            except asyncio.exceptions.TimeoutError:
                await message.clear_reactions()
                return

            emoji = str(res[0].emoji)
            await message.remove_reaction(res[0].emoji, res[1])


def setup(bot: commands.Bot):
    bot.add_cog(Dev(bot))
