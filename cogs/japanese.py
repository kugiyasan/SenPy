import discord
from discord.ext import commands

from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import itertools
import json
import random
import re


class Japanese(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("cogs/gyaru_dict.json") as jsonFile:
            gyaruDict = json.load(jsonFile)

        self.multipleCharacterDict = gyaruDict["multiple_characters"]
        self.singleCharacterDict = gyaruDict["single_character"]

    @commands.command(aliases=["あんき"])
    async def anki(self, ctx, *members: discord.Member):
        """Remind your friends to do their Anki!"""
        for member in members:
            await ctx.send(f"{member.mention}, did you do your anki yet?")

    @commands.command(aliases=["ぎゃる", "ギャル"])
    async def gyaru(self, ctx, *, text="_ _"):
        """まじ卍"""
        # replace with multipleCharacterDict and note the changes in a bool list
        changes = [False] * len(text)
        for k, v in self.multipleCharacterDict.items():
            for m in re.finditer(k, text):
                changes[m.start():m.end()] = [True] * len(k)
            text = text.replace(k, random.choice(v))

        # replace with singleCharacterDict
        # if it isn't already changed by multipleCharacterDict
        output = ""
        for i, c in enumerate(text.upper()):
            if changes[i]:
                output += c
            else:
                output += random.choice(self.singleCharacterDict.get(c, c))

        await ctx.send(output)

    @commands.command(aliases=["はいく", "俳句"])
    async def haiku(self, ctx, *, text):
        """Send your 5-7-5 and boom a clean display of your haiku"""
        font = ImageFont.truetype("media/EPMGOBLD.TTF", 20)

        text = ["　" * i * 2 + string for i, string in enumerate(text.split("\n"))][::-1]
        text = itertools.zip_longest(*text, fillvalue="　")
        text = "\n".join(("　".join(line) for line in text))

        size = ImageDraw.Draw(Image.new("RGB", (1, 1))).textsize(text, font)
        image = Image.new("RGB", (size[0] + 20, size[1] + 20))
        draw = ImageDraw.Draw(image)

        draw.text((5, 5), text, font=font, align="left")

        with BytesIO() as image_binary:
            image.save(image_binary, "PNG")
            image_binary.seek(0)
            file = discord.File(fp=image_binary, filename="haiku.png")

        embed = discord.Embed(color=discord.Color.gold())
        embed.set_image(url="attachment://haiku.png")
        await ctx.send(file=file, embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Japanese(bot))
