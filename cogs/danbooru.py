import discord
from discord.ext import commands

import random
import requests
from cogs.utils.sendEmbed import sendEmbed


class Danbooru(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # categoriesDict = {"category1": "page": 1, "urls": ["url1", "url2"]}
        self.categoriesDict = {}

    @commands.is_nsfw()
    @commands.command()
    async def coconut(self, ctx):
        """Who really wants images of Coconut?"""
        await self.danbooru(ctx, "coconut_%28nekopara%29+")

    @commands.is_nsfw()
    @commands.command()
    async def searchdanbooru(self, ctx, searchWord):
        """Finally a danbooru search command"""
        url = f"https://danbooru.donmai.us/tags.json?search%5Bname_matches%5D={searchWord}*"
        response = requests.get(url)

        if not response.ok:
            print(f"Error {url} responded {response.status_code}")
            raise ConnectionError

    @commands.is_nsfw()
    @commands.command(aliases=["db", "dan"])
    async def danbooru(self, ctx, tags):
        """Wow searching on danbooru that's so original"""
        if not len(self.categoriesDict.get(tags, {}).get("urls", [])):
            try:
                await self.requestDanbooru(tags)
            except Exception as err:
                await ctx.send(err)
                return

        await sendEmbed(ctx, self.categoriesDict[tags]["urls"].pop())

    async def requestDanbooru(self, category):
        print("resquesting danbooru")
        try:
            page = self.categoriesDict[category]["page"]
        except KeyError:
            self.categoriesDict[category] = {"page": 1, "urls": []}
            page = 1

        url = f"https://danbooru.donmai.us/posts.json?page={page}&tags={category}&limit=200"
        response = requests.get(url)

        if not response.ok:
            print(f"Error {url} responded {response.status_code}")
            raise ConnectionError

        if not len(response.json()):
            raise Exception(
                "There is no image with this tag! Be sure to type the exact name!")

        self.categoriesDict[category]["page"] += 1

        for post in response.json():
            if post.get("file_url", None):
                self.categoriesDict[category]["urls"].append(post["file_url"])

        random.shuffle(self.categoriesDict[category]["urls"])
        l = len(self.categoriesDict[category]["urls"])
        print(f"{l} urls for {category}")


def setup(bot: commands.Bot):
    bot.add_cog(Danbooru(bot))
