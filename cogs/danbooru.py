import discord
from discord.ext import commands

from pybooru import Danbooru
import random
import requests
from cogs.utils.sendEmbed import sendEmbed


class DanbooruCog(commands.Cog, name="Danbooru"):
    def __init__(self, bot):
        self.bot = bot
        self.urlsTags = {}
        self.client = Danbooru("danbooru")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Check if the message starts with the command prefix
        pass

    @commands.command()
    async def searchdanbooru(self, ctx, searchWord):
        """Finally a danbooru search command"""
        pass

    @commands.command(aliases=["db", "dan"])
    async def danbooru(self, ctx: commands.Context, *, tags="rating:s"):
        """Wow searching on danbooru that's so original"""
        # f"search[name_matches]={tags}*"

        if not len(self.urlsTags.get(tags, {})):
            await self.requestDanbooru(tags)

        post = self.urlsTags[tags].pop()
        if post["rating"] != "s" and not ctx.channel.is_nsfw():
            raise commands.errors.NSFWChannelRequired(ctx.channel)

        await ctx.send(embed=self.danbooruEmbed(post))

    async def requestDanbooru(self, tags):
        print("resquesting danbooru")

        randompage = random.randint(1, 100)
        posts = self.client.post_list(
            tags=tags, page=randompage, limit=200, random=True)

        if len(posts) < 1:
            print("No posts with those tags")
            return

        if self.urlsTags.get(tags, None) == None:
            self.urlsTags[tags] = []

        keys = ("id", "created_at", "score", "rating",
                "file_url", "tag_string_artist")
        for post in posts:
            try:
                miniPost = {k: post[k] for k in keys}
                self.urlsTags[tags].append(miniPost)
            except:
                pass

        random.shuffle(self.urlsTags[tags])
        print(f"{len(self.urlsTags[tags])} urls for {tags}")

    def danbooruEmbed(self, post):
        print(post["file_url"])
        embed = discord.Embed(
            color=discord.Colour.gold(),
            title=f"source",
            url=f"https://danbooru.donmai.us/posts/{post['id']}"
        )

        embed.set_image(url=post["file_url"])
        embed.set_author(name=post["tag_string_artist"])
        embed.set_footer(text=f'{post["score"]}⬆️')

        return embed


def setup(bot: commands.Bot):
    bot.add_cog(DanbooruCog(bot))
