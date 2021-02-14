import discord
from discord.ext import commands

from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import itertools
import json
from pathlib import Path
import random
import re


class Japanese(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        media = Path(__file__).parent.parent.parent / "media"
        with open(media / "gyaru_dict.json") as jsonFile:
            gyaru_dict = json.load(jsonFile)

        self.multiple_character_dict = gyaru_dict["multiple_characters"]
        self.single_character_dict = gyaru_dict["single_character"]

        self.font_size = 20
        self.font = ImageFont.truetype(str(media / "japanese_font.ttf"), self.font_size)

    @commands.command(aliases=["あんき", "暗記"])
    async def anki(self, ctx, *members: discord.Member):
        """Remind your friends to do their Anki!"""
        for member in members:
            await ctx.send(f"{member.mention}, did you do your anki yet?")

    @commands.command(aliases=["ぎゃる", "ギャル"])
    async def gyaru(self, ctx, *, text="_ _"):
        """まじ卍"""
        # replace with multiple_character_dict and note the changes in a bool list
        changes = [False] * len(text)
        for k, v in self.multiple_character_dict.items():
            for m in re.finditer(k, text):
                changes[m.start() : m.end()] = [True] * len(k)
            text = text.replace(k, random.choice(v))

        # replace with single_character_dict
        # if it isn't already changed by multiple_character_dict
        output = ""
        for i, c in enumerate(text.upper()):
            if changes[i]:
                output += c
            else:
                output += random.choice(self.single_character_dict.get(c, c))

        await ctx.send(output)

    @commands.command(aliases=["はいく", "俳句"])
    async def haiku(self, ctx, *, text):
        """Send your 5-7-5 and boom a clean display of your haiku"""
        # Turn the text top to bottom right to left
        text = ["　" * i * 2 + string for i, string in enumerate(text.split("\n"))][::-1]
        text = itertools.zip_longest(*text, fillvalue="　")
        text = "\n".join(("　".join(line) for line in text))

        # Write the text on a image
        size = ImageDraw.Draw(Image.new("RGB", (1, 1))).textsize(text, self.font)
        image = Image.new("RGB", (size[0] + self.font_size, size[1] + self.font_size))
        draw = ImageDraw.Draw(image)
        draw.text((5, 5), text, font=self.font, align="left")

        # Save the image in the ram
        with BytesIO() as image_binary:
            image.save(image_binary, "PNG")
            image_binary.seek(0)
            image_file = discord.File(fp=image_binary, filename="haiku.png")

        embed = discord.Embed(color=discord.Color.gold())
        embed.set_image(url="attachment://haiku.png")
        await ctx.send(file=image_file, embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Japanese(bot))
