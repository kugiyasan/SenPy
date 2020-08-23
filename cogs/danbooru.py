import discord
from discord.ext import commands

import random
import requests
from cogs.utils.sendEmbed import sendEmbed


class Danbooru(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # categoriesDict = {"category1": "pageCount": 1, "urls": ["url1", "url2"]}
        self.categoriesDict = {}

    @commands.is_nsfw()
    @commands.command()
    async def coconut(self, ctx):
        """Who really wants images of Coconut?"""
        await self.danbooru(ctx, "coconut_%28nekopara%29+")

    @commands.is_nsfw()
    @commands.command()
    async def danbooru(self, ctx, tags):
        """Wow searching on danbooru that's so original"""
        url = f"https://danbooru.donmai.us/posts.json?tags={tags}"
        response = requests.get(url)

        if not response.ok:
            print(f"Error {url} responded {response.status_code}")
            raise ConnectionError

        response = response.json()
        if type(response) == list:
            if not self.categoriesDict.get(tags, None) or not len(self.categoriesDict[tags]["urls"]):
                try:
                    await self.requestDanbooru(tags)
                except Exception as err:
                    await ctx.send(err)
                    return

            await sendEmbed(ctx, self.categoriesDict[tags]["urls"].pop())
        else:
            await ctx.send(response.json()["body"])

    async def requestDanbooru(self, category):
        try:
            page = self.categoriesDict[category]["pageCount"]
        except:
            page = 1

        url = f"https://danbooru.donmai.us/posts.json?page={page}&tags={category}"
        response = requests.get(url)

        if not response.ok:
            print(f"Error {url} responded {response.status_code}")
            raise ConnectionError

        if not self.categoriesDict.get(category, None):
            self.categoriesDict[category] = {"pageCount": 1, "urls": []}

        self.categoriesDict[category]["pageCount"] += 1

        for post in response.json():
            if post.get("file_url", None):
                self.categoriesDict[category]["urls"].append(post["file_url"])

        if not len(self.categoriesDict[category]["urls"]):
            raise Exception(
                "There is no image with this tag! Be sure to type the exact name!")

        random.shuffle(self.categoriesDict[category]["urls"])


def setup(bot: commands.Bot):
    bot.add_cog(Danbooru(bot))
