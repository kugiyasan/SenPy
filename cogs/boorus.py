import discord
from discord.ext import commands

from pybooru import Danbooru, Moebooru
import json
import random
import requests

from cogs.mofupoints import incrementEmbedCounter


class BooruCog(commands.Cog, name="Booru"):
    def __init__(self, bot, Client, site_name, post_url, site_url=""):
        self.bot = bot
        self.site_name = site_name
        self.urlsTags = {}
        self.client = Client(site_name=site_name, site_url=site_url)
        self.post_url = post_url

    async def booru(self, ctx: commands.Context, *, tags="rating:s"):
        """Wow searching on booru site that's so original"""
        if not len(self.urlsTags.get(tags, {})):
            async with ctx.channel.typing():
                await self.requestBooru(tags)

            if not len(self.urlsTags.get(tags, {})):
                await ctx.send("I couldn't find any image with that tag!")
                return

        post = self.urlsTags[tags].pop()
        if not (
            post["rating"] in ("s", "safe")
            or isinstance(ctx.channel, discord.DMChannel)
            or ctx.channel.is_nsfw()
        ):
            raise commands.errors.NSFWChannelRequired(ctx.channel)

        await ctx.send(embed=self.booruEmbed(post))
        incrementEmbedCounter(ctx.author)

    async def requestBooru(self, tags):
        print("requesting " + self.site_name)

        posts = self.client.post_list(tags=tags, limit=100, random=True)
        # print(posts[0])

        if len(posts) < 1:
            print(f"No post with {tags}")
            return

        if self.urlsTags.get(tags, None) is None:
            self.urlsTags[tags] = []

        self.fillUrlsDict(tags, posts)

        random.shuffle(self.urlsTags[tags])
        print(f"{len(self.urlsTags[tags])} urls for {tags}")

    def fillUrlsDict(self, tags, posts):
        keys = ("id", "created_at", "score", "rating", "file_url")
        for post in posts:
            try:
                miniPost = {k: post.get(k, None) for k in keys}
                if miniPost["file_url"] is None:
                    miniPost["file_url"] = (
                        f"https://furry.booru.org//images/{post['directory']}/"
                        + post["image"]
                    )
                miniPost["file_url"] = miniPost["file_url"].replace(" ", "%20")

                if isinstance(self.client, Danbooru):
                    miniPost["author"] = post["tag_string_artist"]
                elif isinstance(self.client, GelbooruClient):
                    miniPost["author"] = post["owner"]
                else:
                    miniPost["author"] = post["author"]

                if post.get("file_size", 0) > 8000000:
                    miniPost["file_url"] = post["preview_url"]

                self.urlsTags[tags].append(miniPost)
            except Exception as err:
                print(err)

    def booruEmbed(self, post):
        post_url = self.post_url + str(post["id"])
        print(post_url)
        print(post["file_url"])
        embed = discord.Embed(color=discord.Colour.gold(), title="sauce", url=post_url)

        embed.set_image(url=post["file_url"])
        embed.set_author(name=post["author"])
        embed.set_footer(text=f'{post["score"]}⬆️ created at: {post["created_at"]}')

        return embed


class DanbooruCog(BooruCog, name="Danbooru"):
    def __init__(self, bot, Client, site_name, post_url):
        super().__init__(bot, Client, site_name, post_url)
        # TODO put the list in the database
        self.shortcuts = {
            "02": "zero_two_(darling_in_the_franxx)",
            "18+": "rating:e",
            "Z23": "Z23_(azur_lane)",
            "akashi": "akashi_(azur_lane) rating:s",
            "aqua": "aqua_(konosuba)",
            "astolfo": "astolfo_(fate)",
            "atago": "atago_(azur_lane)",
            "birb": "minami_kotori",
            "chika": "fujiwara_chika",
            "emilia": "emilia_(re:zero)",
            "hanamaru": "kunikida_hanamaru",
            "korone": "inugami_korone",
            "loliwaifu": "unicorn_(azur_lane)",
            "long_island": "long_island_(azur_lane)",
            "mari": "ohara_mari",
            "maru": "kunikida_hanamaru",
            "megumin": "megumin",
            "nozomi": "toujou_nozomi",
            "rem": "rem_(re:zero)",
            "rinari": "tennouji_rina",
            "ruby": "kurosawa_ruby",
            "ruka": "sarashina_ruka",
            "senko": "senko_(sewayaki_kitsune_no_senko-san)",
            "shinano": "shinano_(azur_lane)",
            "shiro": "shiro_(sewayaki_kitsune_no_senko-san)",
            "sumi": "sakurasawa_sumi",
            "unicorn": "unicorn_(azur_lane)",
            "you": "watanabe_you",
            "zero_two": "zero_two_(darling_in_the_franxx)",
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        ctx = await self.bot.get_context(message)
        if ctx.command is not None or ctx.prefix is None:
            return

        args = ctx.message.content[len(ctx.prefix) :].split(" ")

        if args[0] not in self.shortcuts.keys():
            return

        args = [self.shortcuts.get(arg, arg) for arg in args]

        try:
            if not (
                isinstance(ctx.channel, discord.DMChannel) or ctx.channel.is_nsfw()
            ):
                raise commands.errors.NSFWChannelRequired(ctx.channel)

            await self.booru(ctx, tags=" ".join(args))
        except commands.errors.NSFWChannelRequired as err:
            #! should handle the errors with the default on_command_error
            await ctx.send(err)
            return

    @commands.command(aliases=["shortcuts"])
    async def waifus(self, ctx):
        longestKey = max(len(k) for k in self.shortcuts.keys())
        shortcuts = "**Available shortcuts:**```"
        for k in sorted(self.shortcuts):
            shortcut = f"\n{k}:" + " " * (longestKey - len(k) + 1) + self.shortcuts[k]
            if len(shortcuts + shortcut) > 2000 - 3:
                await ctx.send(shortcuts + "```")
                shortcuts = "```" + shortcut
            else:
                shortcuts += shortcut

        footer = "You can add your waifus using xd addshortcut :)"
        if len(shortcuts + footer) > 2000 - 3:
            await ctx.send(shortcuts + "```")
            shortcuts = ""

        await ctx.send(shortcuts + "```" + footer)

    @commands.cooldown(5, 3600.0, commands.BucketType.user)
    @commands.command()
    async def addshortcut(self, ctx, key, danbooruTags):
        """add a shortcut for your waifu. 1 hour cooldown after 5 calls"""
        if self.shortcuts.get(key, None):
            await ctx.send("There is already a shortcut with that key!")
        elif self.bot.get_command(key):
            await ctx.send("You can't name a shortcut with the name of a command!")
        elif len(key) > 20:
            await ctx.send("The key is too long, make it 20 characters or less")
        else:
            self.shortcuts[key] = danbooruTags
            await ctx.message.add_reaction("✅")

    @commands.is_owner()
    @commands.command(hidden=True)
    async def delshortcut(self, ctx, key):
        if not self.shortcuts.get(key, None):
            await ctx.send("The shortcut doesn't exist!")
            return

        del self.shortcuts[key]
        await ctx.message.add_reaction("✅")

    @commands.is_nsfw()
    @commands.command(aliases=["dan", "db"])
    async def danbooru(self, ctx, *, tags="rating:s"):
        """Wow searching on danbooru that's so original"""
        await self.booru(ctx, tags=tags)


class Yandere(BooruCog, name="Booru"):
    @commands.is_nsfw()
    @commands.command(aliases=["yan"])
    async def yandere(self, ctx, *, tags="rating:s"):
        """Wow searching on yandere that's so original"""
        await self.booru(ctx, tags=tags)


class Konachan(BooruCog, name="Booru"):
    @commands.is_nsfw()
    @commands.command(aliases=["kon"])
    async def konachan(self, ctx, *, tags="rating:s"):
        """Wow searching on konachan that's so original"""
        await self.booru(ctx, tags=tags)


class Safebooru(BooruCog, name="Booru"):
    @commands.is_nsfw()
    @commands.command(aliases=["safe", "sb"])
    async def safebooru(self, ctx, *, tags="rating:s"):
        """Wow searching on safebooru that's so original"""
        await self.booru(ctx, tags=tags)


class GelbooruClient(object):
    def __init__(self, *, site_name, site_url):
        self.site_name = site_name
        self.site_url = site_url

    def post_list(self, *, limit=200, page=None, tags="", random=False):
        res = requests.get(
            f"https://{self.site_url}/index.php?page=dapi&s=post&q=index&limit={limit}&tags={tags}&json=1"
        )
        return json.loads(res.content)


class Gelbooru(BooruCog, name="Booru"):
    @commands.is_nsfw()
    @commands.command(aliases=["gel", "gb"])
    async def gelbooru(self, ctx, *, tags="unicorn_(azur_lane)"):
        """Wow searching on gelbooru that's so original"""
        await self.booru(ctx, tags=tags)


class Furrybooru(BooruCog, name="Booru"):
    @commands.is_nsfw()
    @commands.command(aliases=["fur"])
    async def furrybooru(self, ctx, *, tags="puro_(changed)"):
        """Wow searching on furrybooru that's so original"""
        await self.booru(ctx, tags=tags)


def setup(bot: commands.Bot):
    bot.add_cog(
        DanbooruCog(bot, Danbooru, "danbooru", "https://danbooru.donmai.us/posts/")
    )
    bot.add_cog(Yandere(bot, Moebooru, "yandere", "https://yande.re/post/show/"))
    bot.add_cog(Konachan(bot, Moebooru, "konachan", "https://konachan.com/post/show/"))
    bot.add_cog(
        Safebooru(bot, Danbooru, "safebooru", "https://safebooru.donmai.us/posts/")
    )
    bot.add_cog(
        Gelbooru(
            bot,
            GelbooruClient,
            "gelbooru",
            "https://gelbooru.com/index.php?page=post&s=view&id=",
            "gelbooru.com",
        )
    )
    bot.add_cog(
        Furrybooru(
            bot,
            GelbooruClient,
            "furrybooru",
            "https://furry.booru.org/index.php?page=post&s=view&id=",
            "furry.booru.org",
        )
    )
