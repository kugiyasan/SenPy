import discord
from discord.ext import commands

from cogs.utils.sendEmbed import sendEmbed
from cogs.utils.deleteMessage import deleteMessage
# from cogs.utils.dbms import *

import asyncio
from fake_useragent import UserAgent
import random
import requests
import sqlite3

class RedditAPI(commands.Cog, name='reddit'):
    def __init__(self, bot):
        self.bot = bot
        self.ua = UserAgent()
        self.URLdata = {}

        #* asyncio.run in python 3.7
        # loop = asyncio.get_event_loop()
        # result = loop.run_until_complete(self.getUrls('ChurchOfSenko', 'ChikaFujiwara', 'OneTrueRem'))

    @commands.command(aliases=['mofu'])
    async def mofumofu(self, ctx: commands.Context, dayNumber: int = 0):
        """Send blessing to the server!"""
        if dayNumber:
            await ctx.send(f'DAY {dayNumber} OF THE OWNER NOT REMOVING THIS CHANNEL')
        await self.sendRedditImage(ctx, 'ChurchOfSenko')

    # def refillURLs(self):
    #     while len(self.URLdata) < 50:
    #         # self.getUrls('ChurchOfSenko')
    #         self.getUrls('ChikaFujiwara')
    #     random.shuffle(self.URLdata)

    @commands.command(name='r/')
    async def sendRedditImage(self, ctx: commands.Context, subreddit):
        '''Try ChurchOfSenko, ChikaFujiwara or OneTrueRem'''
        await deleteMessage(ctx)
        url = await self.getRandomURLFromDB(subreddit)
        await sendEmbed(ctx, url[0])

    async def getUrls(self, *subreddits):
        #* async for in python 3.7
        for subreddit in subreddits:
            after = 'null'
            requestURL = f'https://www.reddit.com/r/{subreddit}/new/.json?limit=100&after={after}'
            print('requesting json file to reddit')
            response = requests.get(requestURL, headers={'User-agent': self.ua.random})

            if not response.ok:
                print(f"Error {requestURL} responded {response.status_code}")
                return

            data = response.json()['data']
            self.after = data['after']
            for child in data['children']:
                image_url = child['data']['url']
                print(image_url)
                exts = ['.png', '.jpg', '.jpeg']
                for ext in exts:
                    if image_url.endswith(ext):
                        await self.addToDatabase(c, subreddit, child['data']['name'], image_url)
                        breakpoint
            
            print(f'{length} urls in the list for {subreddit}')

def setup(bot):
    bot.add_cog(RedditAPI(bot))
