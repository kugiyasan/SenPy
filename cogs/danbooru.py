import discord
from discord.ext import commands

import random
import requests
from cogs.utils.sendEmbed import sendEmbed

class Danbooru(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coconutPageCount = 1
        self.coconutURLs = []

    # @commands.command()
    # async def danbooru(self, ctx, tags):
    #     """Says hello"""
    #     pass
    
    @commands.is_nsfw()
    @commands.command(aliases=["cockonut"])
    async def coconut(self, ctx):
        """Who really wants images of Coconut?"""
        if ctx.author.id == 276038064273489930:
            await ctx.send("No Cockconut pics for Clovis")
            return

        if not len(self.coconutURLs):
            url = f"https://danbooru.donmai.us/posts.json?page={self.coconutPageCount}&tags=coconut_%28nekopara%29+"
            await self.requestDanbooru(url)
            self.coconutPageCount += 1

        await sendEmbed(ctx, self.coconutURLs.pop())


    async def requestDanbooru(self, url):
        response = requests.get(url)

        if not response.ok:
            print(f"Error {url} responded {response.status_code}")
            raise ConnectionError

        for post in response.json():
            if post.get("file_url", None):
                self.coconutURLs.append(post["file_url"])

        if not len(self.coconutURLs):
            raise Exception("There is no more image of Coconut!")

        random.shuffle(self.coconutURLs)


def setup(bot):
    bot.add_cog(Danbooru(bot))