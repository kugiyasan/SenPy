import discord
from discord.ext import commands

from fake_useragent import UserAgent
import random
import requests

class RedditAPI(commands.Cog, name='reddit'):
    def __init__(self, bot):
        self.bot = bot
        self.ua = UserAgent()
        self.after = 'null'
        self.URLdata = []
        # TODO should save URLs locally and maybe even images
        # self.refillURLs()

    @commands.command(name='mofumofu', aliases=['mofu'])
    async def sendPic(self, ctx: commands.Context):
        """Send blessing to the server!"""
        # if self.bot.
        # await ctx.message.delete()
        self.refillURLs()

        e = discord.Embed(
            type='image',
            color=discord.Colour.gold())
        e.set_image(url=self.URLdata.pop())
        await ctx.send(embed=e)

    def refillURLs(self):
        while len(self.URLdata) < 50:
            self.getUrls('ChurchOfSenko')
        random.shuffle(self.URLdata)

    def getUrls(self, subreddit):
        url = f'https://www.reddit.com/r/{subreddit}/new/.json?limit=100&after={self.after}'
        print('requesting json file to reddit')
        response = requests.get(url, headers={'User-agent': self.ua.random})

        if not response.ok:
            print("Error check the name of the subreddit", response.status_code)
            return

        data = response.json()['data']
        self.after = data['after']
        for child in data['children']:
            image_url = child['data']['url']
            print(image_url)
            if 'imgur' in image_url:
                image_url += '.jpeg'
            if '.png' in image_url or '.jpg' in image_url or '.jpeg' in image_url:
                self.URLdata.append(image_url)
        print(f'{len(self.URLdata)} urls in the list')

def setup(bot):
    bot.add_cog(RedditAPI(bot))
