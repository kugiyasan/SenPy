import discord
from discord.ext import commands

from fake_useragent import UserAgent
import io
import random
import requests
# import praw

class RedditAPI(commands.Cog, name='reddit'):
    def __init__(self, bot):
        self.bot = bot
        self.ua = UserAgent()
        self.after = 'null'
        self.URLdata = []
        # TODO should save URLs locally and maybe even images
        # self.refillURLs()

    @commands.command(name='mofumofu')
    async def sendPic(self, ctx: commands.Context):
        """Send blessing to the server!"""
        await ctx.message.delete()
        async with ctx.typing():
            self.refillURLs()

            print('requesting an image to reddit')
            image = requests.get(self.URLdata.pop(), allow_redirects=False)
            if(image.status_code == 200):
                try:
                    discordImage = discord.File(io.BytesIO(image.content), filename='praiseTheLord.png')
                    await ctx.send(file=discordImage)
                    return
                except:
                    print('Error image not sent')
            else:
                print('Error not the good status code 200 !=', image.status_code)

    def refillURLs(self):
        while len(self.URLdata) < 50:
            self.getUrls('ChurchOfSenko')
        random.shuffle(self.URLdata)

    def getUrls(self, subreddit):
        url = f'https://www.reddit.com/r/{subreddit}/new/.json?after={self.after}'
        print('requesting json file to reddit')
        response = requests.get(url, headers={'User-agent': self.ua.random})

        if not response.ok:
            print("Error check the name of the subreddit", response.status_code)
            return

        data = response.json()['data']['children']
        self.after = response.json()['data']['after']
        for child in data:
            image_url = child['data']['url']
            if 'imgur' in image_url:
                image_url += '.jpeg'
            if '.png' in image_url or '.jpg' in image_url or '.jpeg' in image_url:
                self.URLdata.append(image_url)
        print(f'{len(self.URLdata)} urls in the list')

def setup(bot):
    bot.add_cog(RedditAPI(bot))
