import discord
from discord.ext import commands

from cogs.utils.sendEmbed import sendEmbed
from cogs.utils.deleteMessage import deleteMessage

from fake_useragent import UserAgent
import requests

class RedditAPI(commands.Cog, name='reddit'):
    def __init__(self, bot):
        self.bot = bot
        self.ua = UserAgent()
        self.URLdata = {}

    @commands.command()
    async def search(self, ctx, *searchkws):
        '''Search a subreddit name, can help if you get an error with r/'''
        print('requesting search to reddit')
        requestURL = 'https://www.reddit.com/subreddits/search.json?q={}&include_over_18=on'.format('%20'.join(searchkws))

        output = []
        children = await self.requestReddit(requestURL)
        for child in children[:5]:
            subredditName = child['data']['url'][3:-1]
            output.append(subredditName)
        await ctx.send('\n'.join(output))

    @commands.command(aliases=['mofu'])
    async def mofumofu(self, ctx: commands.Context, dayNumber: int = 0):
        """Send blessing to the server!"""
        if dayNumber:
            await ctx.send(f'DAY {dayNumber} OF THE OWNER NOT REMOVING THIS CHANNEL')
        await self.sendRedditImage(ctx, 'ChurchOfSenko')

    @commands.command(name='r/', aliases=['bruh'])
    async def sendRedditImage(self, ctx: commands.Context, subreddit):
        '''Enter the name of a subreddit and get a random pic back!'''
        await deleteMessage(ctx)

        if not self.URLdata.get(subreddit):
            await self.getUrls(subreddit)

        if self.URLdata[subreddit] == []:
            await self.getUrls(subreddit)
            if self.URLdata[subreddit] == []:
                await ctx.send('No subreddit matches this name or there wasn\'t any image!')
                return

        url = self.URLdata[subreddit].pop()
        if url.startswith('NSFW'):
            if not ctx.channel.is_nsfw():
                await ctx.send('Retry in a nsfw channel with this subreddit!')
                self.URLdata[subreddit].append(url)
                return
            else:
                url = url[4:]
    
        await sendEmbed(ctx, url)

    async def requestReddit(self, url):
        print('requesting reddit')
        response = requests.get(url, headers={'User-agent': self.ua.random})

        if not response.ok:
            print(f"Error {url} responded {response.status_code}")
            raise ConnectionError

        return response.json()['data']['children']

    async def getUrls(self, subreddit):
        requestURL = f'https://www.reddit.com/r/{subreddit}/randomrising/.json?kind=t3'
        response = await self.requestReddit(requestURL)
        nsfwCount = 0

        if not self.URLdata.get(subreddit):
            self.URLdata[subreddit] = []

        for child in response:
            image_url = child['data']['url']

            if child['data']['over_18']:
                image_url = 'NSFW' + image_url
                nsfwCount += 1

            exts = ['.png', '.jpg', '.jpeg']
            for ext in exts:
                if image_url.endswith(ext):
                    self.URLdata[subreddit].append(image_url)
                    break
        
        print(f'{len(self.URLdata[subreddit])} urls in the list for {subreddit} ({nsfwCount} of them are nsfw)')

def setup(bot):
    bot.add_cog(RedditAPI(bot))
