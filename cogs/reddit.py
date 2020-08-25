import discord
from discord.ext import commands, tasks

from cogs.utils.deleteMessage import deleteMessage
from cogs.utils.prettyList import prettyList
from cogs.mofupoints import incrementEmbedCounter

import asyncio
from fake_useragent import UserAgent
import inspect
import random
import re
import requests


class RedditAPI(commands.Cog, name="Reddit"):
    def __init__(self, bot):
        self.bot = bot
        self.ua = UserAgent(verify_ssl=False)
        self.urls = {}
        self.waifuByTheHour.start()

    def cog_unload(self):
        self.waifuByTheHour.cancel()

    @tasks.loop(hours=1.0)
    async def waifuByTheHour(self):
        channel = self.bot.get_channel(722374291148111884)

        if not channel:
            return

        subreddits = ("ChikaFujiwara", "ZeroTwo")
        subreddit = random.choice(subreddits)
        await self.sendRedditImage(channel, subreddit, dropnsfw=True)

    @waifuByTheHour.before_loop
    async def before_waifuByTheHour(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(1)

    @commands.command(aliases=["ara"])
    async def araara(self, ctx: commands.Context):
        """Ara ara you want a description of this command?"""
        subreddits = ("AnimeMILFS", "AraAra")
        await self.sendRedditImage(ctx, random.choice(subreddits))

    @commands.command(aliases=["mofu"])
    async def mofumofu(self, ctx: commands.Context):
        """Send blessing to the server!"""
        subreddits = ("senko", "SewayakiKitsune",
                      "ChurchOfSenko", "fluffthetail")
        await self.sendRedditImage(ctx, random.choice(subreddits))

    @commands.command(aliases=["sub"])
    async def subreddit(self, ctx, *, subreddit="all"):
        """Get a random pic from a subreddit!"""
        await self.sendRedditImage(ctx, subreddit)

    @commands.command(aliases=["reddit"])
    async def search(self, ctx, *searchkws):
        """Search a subreddit name"""
        if not len(searchkws):
            raise commands.errors.MissingRequiredArgument(
                inspect.Parameter("searchkws", inspect.Parameter.POSITIONAL_ONLY))

        print("requesting search to reddit")
        requestURL = f"https://www.reddit.com/subreddits/search.json?q={'%20'.join(searchkws)}&include_over_18=on"
        NUMBER_OF_SUGGESTIONS = 5

        children = await self.requestReddit(requestURL)
        suggestions = [child["data"]["url"][3:-1]
                       for child in children[:NUMBER_OF_SUGGESTIONS]]

        NUMBER_OF_SUGGESTIONS = len(suggestions)

        title = f"**Top {NUMBER_OF_SUGGESTIONS} subreddits based on your search keyword (Select with 1-{NUMBER_OF_SUGGESTIONS}):**"
        await prettyList(ctx, title, suggestions, maxLength=NUMBER_OF_SUGGESTIONS)

        def checkresponse(m):
            return (m.author == ctx.author
                    and m.channel == ctx.channel
                    and m.content.isdecimal()
                    and int(m.content) > 0
                    and int(m.content) <= NUMBER_OF_SUGGESTIONS)

        try:
            m = await self.bot.wait_for("message", timeout=60.0, check=checkresponse)
        except:
            return

        await self.sendRedditImage(ctx, suggestions[int(m.content)-1])

    async def sendRedditImage(self, ctx: commands.Context, subreddit="all", dropnsfw=False):
        subreddit = subreddit.lower()

        try:
            if not self.urls.get(subreddit):
                await self.getSubredditURLs(subreddit)

            if self.urls[subreddit] == []:
                await self.getSubredditURLs(subreddit)
                if not len(self.urls[subreddit]):
                    await ctx.send("There wasn't any image in this subreddit!")
                    return
        except ConnectionError:
            await ctx.send("No subreddit matches this name!")
            return

        post = self.urls[subreddit].pop()
        if dropnsfw:
            while post["over_18"]:
                post = self.urls[subreddit].pop()

                if self.urls == []:
                    await ctx.send(f"No SFW image on r/{subreddit}!")
                    return

        if post["over_18"]:
            try:
                nsfwChannel = ctx.channel.is_nsfw()
            except:
                nsfwChannel = ctx.is_nsfw()

            if not nsfwChannel:
                await ctx.send("Retry in a nsfw channel with this subreddit!")
                self.urls[subreddit].append(post)
                return

        if hasattr(ctx, "author"):
            await incrementEmbedCounter(ctx.author)

        await ctx.send(embed=await self.redditEmbed(subreddit, post))

    async def redditEmbed(self, subreddit, post):
        embed = discord.Embed(
            color=discord.Colour.gold(),
            title=f"r/{subreddit}",
            description=f"[{post['title']}](https://reddit.com{post['permalink']})",
            url=f"https://reddit.com/r/{subreddit}")

        embed.set_image(url=post["url"])
        embed.set_author(
            name=post["author"],
            url=f"https://reddit.com/u/{post['author']}"
        )
        embed.set_footer(
            text=f'{post["score"]}⬆️ {post["num_comments"]}💬')

    async def requestReddit(self, url):
        print("requesting reddit")
        response = requests.get(url, headers={"User-agent": self.ua.random})

        if not response.ok:
            print(f"Error {url} responded {response.status_code}")
            raise ConnectionError

        return response.json()["data"]["children"]

    async def getSubredditURLs(self, subreddit):
        requestURL = f"https://www.reddit.com/r/{subreddit}/randomrising/.json?kind=t3"

        response = await self.requestReddit(requestURL)

        if not self.urls.get(subreddit):
            self.urls[subreddit] = []

        fields = ("title", "score", "over_18", "author",
                  "num_comments", "permalink", "url")
        for child in response:
            postInfo = {}
            if not re.search(r"(\.jpg|\.png|\.jpeg|\.gif)$", child["data"]["url"]):
                print(child["data"]["url"])
                continue

            for field in fields:
                postInfo[field] = child["data"][field]

            self.urls[subreddit].append(postInfo)

        print(f"{len(self.urls[subreddit])} urls for r/{subreddit}")


def setup(bot: commands.Bot):
    bot.add_cog(RedditAPI(bot))
