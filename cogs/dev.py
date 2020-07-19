import discord
from discord.ext import commands
import asyncio

from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import itertools
import sys

class Dev(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        pass
        # print(discord.Permissions.send_messages)

    @commands.command(hidden=True)
    async def test(self, ctx: commands.Context):
        file = discord.File("media/hanamaru.jpg", filename="image.png")
        embed = discord.Embed()
        embed.set_image(url="attachment://image.png")
        await ctx.send(file=file, embed=embed)

    @commands.command(hidden=True)
    async def haiku(self, ctx, *, text):
        if sys.platform == "win32":
            font = ImageFont.truetype(r"C:\Windows\Fonts\msgothic.ttc", 20)
        elif sys.platform == "linux":
            font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", 20)
        else:
            await ctx.send("This command doesn't work on this bot operating system")
            return

        text = itertools.zip_longest(*text.split("\n")[::-1], fillvalue="　")
        text = "\n".join(("　".join(line) for line in text))

        size = ImageDraw.Draw(Image.new("RGB", (1, 1))).textsize(text, font)
        image = Image.new('RGB', (size[0]+20, size[1]+20))
        draw = ImageDraw.Draw(image)

        draw.text((5, 5), text, font=font, align="left")

        with BytesIO() as image_binary:
            image.save(image_binary, 'PNG')
            image_binary.seek(0)
            file = discord.File(fp=image_binary, filename="haiku.png")
            embed = discord.Embed()
            embed.set_image(url="attachment://haiku.png")
            await ctx.send(file=file, embed=embed)

    @commands.command(hidden=True)
    async def e(self, ctx: commands.Context):
        page1 = discord.Embed(
            title='Page 1/3',
            description='Description',
            colour=discord.Colour.orange()
        )
        page2 = discord.Embed(
            title='Page 2/3',
            description='Description',
            colour=discord.Colour.gold()
        )
        page3 = discord.Embed(
            title='Page 3/3',
            description='Description',
            colour=discord.Colour.orange()
        )

        pages = [page1, page2, page3]

        message = await ctx.send(embed=page1)
        await message.add_reaction('\u23ee')
        await message.add_reaction('\u25c0')
        await message.add_reaction('\u25b6')
        await message.add_reaction('\u23ed')

        i = 0
        emoji = ''

        while True:
            if emoji == '\u23ee':
                i = 0
                await message.edit(embed=pages[i])
            if emoji == '\u25c0':
                if i > 0:
                    i -= 1
                    await message.edit(embed=pages[i])
            if emoji == '\u25b6':
                if i < 2:
                    i += 1
                    await message.edit(embed=pages[i])
            if emoji == '\u23ed':
                i = 2
                await message.edit(embed=pages[i])

            def check(reaction, member):
                return ctx.author == member

            try:
                res = await self.bot.wait_for('reaction_add', check=check, timeout=30)
            except asyncio.exceptions.TimeoutError:
                await message.clear_reactions()
                return

            emoji = str(res[0].emoji)
            await message.remove_reaction(res[0].emoji, res[1])


def setup(bot):
    bot.add_cog(Dev(bot))
