import discord
from discord.ext import commands

from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import itertools

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def haiku(self, ctx, *, text):
        font = ImageFont.truetype("media/Sword.ttf", 20)

        text = itertools.zip_longest(*text.split("\n")[::-1], fillvalue="　")
        text = "\n".join(("".join(line) for line in text))

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

def setup(bot):
    bot.add_cog(Greetings(bot))