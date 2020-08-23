import discord
from discord.ext import commands

from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import itertools


class Japanese(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def haiku(self, ctx, *, text):
        """Send your 5-7-5 and boom a clean display of your haiku"""
        font = ImageFont.truetype("media/EPMGOBLD.TTF", 20)

        text = ["　"*i*2 + string for i, string in enumerate(text.split("\n"))][::-1]
        text = itertools.zip_longest(*text, fillvalue="　")
        text = "\n".join(("　".join(line) for line in text))

        size = ImageDraw.Draw(Image.new("RGB", (1, 1))).textsize(text, font)
        image = Image.new('RGB', (size[0]+20, size[1]+20))
        draw = ImageDraw.Draw(image)

        draw.text((5, 5), text, font=font, align="left")

        with BytesIO() as image_binary:
            image.save(image_binary, 'PNG')
            image_binary.seek(0)
            file = discord.File(fp=image_binary, filename="haiku.png")

        embed = discord.Embed(color=discord.Color.gold())
        embed.set_image(url="attachment://haiku.png")
        await ctx.send(file=file, embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Japanese(bot))
