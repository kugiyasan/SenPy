import discord
from discord.ext import commands

from cogs.utils.sendEmbed import sendEmbed
from cogs.utils.deleteMessage import deleteMessage
from cogs.utils.dbms import *

import asyncio
from fake_useragent import UserAgent
import random
import requests
import sqlite3

class RedditAPI(commands.Cog, name='reddit'):
    def __init__(self, bot):
        self.bot = bot
        self.ua = UserAgent()
        # self.after = 'null'
        # self.URLdata = []
        # TODO should save URLs locally
        # self.refillURLs()
        #* asyncio.run in python 3.7
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.getUrls('ChurchOfSenko', 'ChikaFujiwara', 'OneTrueRem'))

    @commands.command(aliases=['mofu'])
    async def mofumofu(self, ctx: commands.Context, dayNumber: int = 0):
        """Send blessing to the server!"""
        if dayNumber:
            await ctx.send(f'DAY {dayNumber} OF THE OWNER NOT REMOVING THIS CHANNEL')
        await self.sendRedditImage(ctx, 'ChurchOfSenko')
        # self.refillURLs()
        # await sendEmbed(ctx, self.URLdata.pop())
        # url = c.execute('SELECT * FROM ChurchOfSenko ORDER BY RANDOM() LIMIT 1')
        # await sendEmbed(ctx, url)

    # def refillURLs(self):
    #     while len(self.URLdata) < 50:
    #         # self.getUrls('ChurchOfSenko')
    #         self.getUrls('ChikaFujiwara')
    #     random.shuffle(self.URLdata)

    @commands.command(name='r/')
    async def sendRedditImage(self, ctx: commands.Context, subreddit):
        await deleteMessage(ctx)
        url = self.getRandomURLFromDB(subreddit)
        await sendEmbed(ctx, url)

    @database
    def getRandomURLFromDB(self, c, subreddit):
        q = c.execute('SELECT url FROM ? ORDER BY RANDOM() LIMIT 1', (subreddit,))
        print(q)
        return q

    @database
    async def getUrls(self, c, garbageSelf, *subreddits):
        #* async for in python 3.7
        for subreddit in subreddits:
            print(subreddit, subreddits)
            # query = "SELECT * FROM {} ORDER BY column DESC LIMIT 1".format(subreddit)
            # c.execute(query)
            # after = c.fetchall()
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
                        break
            query = 'SELECT COUNT(*) FROM {}'.format(subreddit)
            c.execute(query)
            length = c.fetchone()[0]
            print(f'{length} urls in the list for {subreddit}')

    async def addToDatabase(self, c, subreddit, name, url):
        c.execute("SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name=?", (subreddit,))
        tableExists = c.fetchone()
        print(tableExists)
        if tableExists == (0,):
            query = "CREATE TABLE {} (name text, url text)".format(subreddit)
            c.execute(query)
        query = "INSERT INTO {} VALUES (?,?)".format(subreddit)
        # print(query)
        c.execute(query, (name, url))


def setup(bot):
    bot.add_cog(RedditAPI(bot))
