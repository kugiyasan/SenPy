import discord
from discord.ext import commands

from pybooru import Danbooru, Moebooru, PybooruHTTPError
import json
import requests

from .mofupoints import incrementEmbedCounter


class BooruCog(commands.Cog, name="Booru"):
    def __init__(self, bot: commands.Bot, Client: "BooruCog", site_name: str, post_url: str, site_url: str="") -> None:
        self.bot = bot
        self.site_name = site_name
        self.urlsTags = {}
        self.client = Client(site_name=site_name, site_url=site_url)
        self.post_url = post_url

    async def booru(self, ctx: commands.Context, *, tags: str="rating:s") -> None:
        """Wow searching on booru site that's so original"""
        if not len(self.urlsTags.get(tags, {})):
            async with ctx.channel.typing():
                self.requestBooru(tags)

            if not len(self.urlsTags.get(tags, {})):
                await ctx.send("I couldn't find any image with that tag!")
                return

        post = self.urlsTags[tags].pop()
        if not (
            post["rating"] in ("s", "safe")
            or not isinstance(ctx.channel, discord.TextChannel)
            or ctx.channel.is_nsfw()
        ):
            raise commands.errors.NSFWChannelRequired(ctx.channel)

        await self.sendBooruEmbed(ctx, post)
        incrementEmbedCounter(ctx.author)

    def requestBooru(self, tags: str) -> None:
        print("requesting " + self.site_name)

        try:
            posts = self.client.post_list(tags=tags, limit=100, random=True)
        except PybooruHTTPError as error:
            print(error)
            return
        # print(posts[0])

        if len(posts) < 1:
            print(f"No post with {tags}")
            return

        if self.urlsTags.get(tags) is None:
            self.urlsTags[tags] = []

        self.fillUrlsDict(tags, posts)

        print(f"{len(self.urlsTags[tags])} urls for {tags}")

    def fillUrlsDict(self, tags, posts):
        keys = ("id", "created_at", "score", "rating", "file_url")
        for post in posts:
            try:
                miniPost = {k: post.get(k) for k in keys}
                if not miniPost["file_url"]:
                    return
                if miniPost["file_url"].endswith(".zip"):
                    miniPost["file_url"] = post["large_file_url"]
                miniPost["file_url"] = miniPost["file_url"].replace(" ", "%20")

                if isinstance(self.client, Danbooru):
                    miniPost["author"] = post["tag_string_artist"]
                elif isinstance(self.client, GelbooruClient):
                    miniPost["author"] = post["owner"]
                else:
                    miniPost["author"] = post["author"]

                if post.get("file_size", 0) > 8000000:
                    miniPost["file_url"] = post.get("preview_url", miniPost["file_url"])

                self.urlsTags[tags].append(miniPost)
            except Exception as err:
                print(err)

    async def sendBooruEmbed(self, ctx, post):
        post_url = self.post_url + str(post["id"])
        print(post_url)
        print(post["file_url"])
        embed = discord.Embed(color=discord.Colour.gold(), title="sauce", url=post_url)

        embed.set_author(name=post["author"])
        embed.set_footer(text=f'{post["score"]}⬆️ created at: {post["created_at"]}')
        embed.set_image(url=post["file_url"])

        if post["file_url"].endswith(".mp4") or post["file_url"].endswith(".webm"):
            await ctx.send(post["file_url"])

        await ctx.send(embed=embed)


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
            "k": "kisaragi_(azur_lane) rating:s",
            "kisaragi": "kisaragi_(azur_lane) rating:s",
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
            # ! should handle the errors with the default on_command_error
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
        if self.shortcuts.get(key):
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
        if not self.shortcuts.get(key):
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
        tags = (
            (tags + " ")
            .replace("rating:s ", "rating:safe ")
            .replace("rating:q ", "rating:questionnable ")
            .replace("rating:e ", "rating:explicit ")
        )
        print(tags)
        res = requests.get(
            f"https://{self.site_url}/index.php?"
            f"page=dapi&s=post&q=index&limit={limit}&tags={tags}&json=1"
        )
        return json.loads(res.content) if res.content else []


class Gelbooru(BooruCog, name="Booru"):
    @commands.is_nsfw()
    @commands.command(aliases=["gel", "gb"])
    async def gelbooru(self, ctx, *, tags="unicorn_(azur_lane)"):
        """Wow searching on gelbooru that's so original"""
        await self.booru(ctx, tags=tags)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        DanbooruCog(bot, Danbooru, "danbooru", "https://danbooru.donmai.us/posts/")
    )
    # await bot.add_cog(Yandere(bot, Moebooru, "yandere", "https://yande.re/post/show/"))
    # await bot.add_cog(Konachan(bot, Moebooru, "konachan", "https://konachan.com/post/show/"))
    # await bot.add_cog(
    #     Safebooru(bot, Danbooru, "safebooru", "https://safebooru.donmai.us/posts/")
    # )
    # await bot.add_cog(
    #     Gelbooru(
    #         bot,
    #         GelbooruClient,
    #         "gelbooru",
    #         "https://gelbooru.com/index.php?page=post&s=view&id=",
    #         "gelbooru.com",
    #     )
    # )
