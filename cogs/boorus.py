import discord
from discord.ext import commands

from pybooru import Danbooru, Moebooru
import functools
import random
import requests
import time

from cogs.utils.sendEmbed import sendEmbed
from cogs.mofupoints import incrementEmbedCounter

clovisProtection = False


def booruCommandName(func):
    # https://stackoverflow.com/questions/42043226/using-a-coroutine-as-decorator
    @functools.wraps(func)
    async def wrapped(self, *args, **kwargs):
        return await func(self, *args, **kwargs)
    return wrapped


class BooruCog(commands.Cog, name="Booru"):
    def __init__(self, bot, Client, site_name, post_url, site_url=""):
        self.bot = bot
        self.site_name = site_name
        self.urlsTags = {}
        self.client = Client(site_name, site_url)
        self.post_url = post_url

    # @commands.command(name=self.site_name, aliases=self.aliases)
    # @commands.is_nsfw()
    # @booruCommandName
    async def booru(self, ctx: commands.Context, *, tags="rating:s"):
        """Wow searching on booru site that's so original"""
        if not len(self.urlsTags.get(tags, {})):
            async with ctx.channel.typing():
                await self.requestBooru(tags)

            if not len(self.urlsTags.get(tags, {})):
                await ctx.send("I couldn't find any image with that tag!")
                return

        post = self.urlsTags[tags].pop()
        if (post["rating"] != "s"
                and not isinstance(ctx.channel, discord.DMChannel)
                and not ctx.channel.is_nsfw()):
            raise commands.errors.NSFWChannelRequired(ctx.channel)

        if ctx.author.id == 276038064273489930 and clovisProtection == True:
            if "rating:e" in tags:
                await ctx.send("I couldn't find any image with that tag!")
                return

            while post["rating"] == "e":
                print(f"dropping {post}")
                post = self.urlsTags[tags].pop()

        await ctx.send(embed=self.booruEmbed(post))
        await incrementEmbedCounter(ctx.author)

    async def requestBooru(self, tags):
        print("requesting " + self.site_name)

        posts = self.client.post_list(tags=tags, limit=100, random=True)
        # print(posts[0])

        if len(posts) < 1:
            print(f"No post with {tags}")
            return

        if self.urlsTags.get(tags, None) == None:
            self.urlsTags[tags] = []

        keys = ("id", "created_at", "score", "rating", "file_url")
        for post in posts:
            try:
                miniPost = {k: post[k] for k in keys}

                if isinstance(self.client, Danbooru):
                    miniPost["author"] = post["tag_string_artist"]
                else:
                    miniPost["author"] = post["author"]
                if self.site_name == "yandere":
                    # file_url is too slow to load on yande.re
                    miniPost["file_url"] = post["preview_url"]

                self.urlsTags[tags].append(miniPost)
            except:
                pass

        random.shuffle(self.urlsTags[tags])
        print(f"{len(self.urlsTags[tags])} urls for {tags}")

    def booruEmbed(self, post):
        post_url = self.post_url + str(post['id'])
        print(post_url)
        embed = discord.Embed(
            color=discord.Colour.gold(),
            title=f"sauce",
            url=post_url
        )

        embed.set_image(url=post["file_url"])
        embed.set_author(name=post["author"])
        embed.set_footer(
            text=f'{post["score"]}⬆️ created at: {post["created_at"]}')

        return embed


class DanbooruCog(BooruCog, name="Danbooru"):
    def __init__(self, bot):
        super().__init__(bot, Danbooru, "danbooru", "https://danbooru.donmai.us/posts/")
        self.shortcuts = {
            "02": "zero_two_(darling_in_the_franxx)",
            "akashi": "akashi_(azur_lane)",
            "chika": "fujiwara_chika",
            "emilia": "emilia_(re:zero)",
            "hanamaru": "kunikida_hanamaru",
            "korone": "inugami_korone",
            "maru": "kunikida_hanamaru",
            "megumin": "megumin",
            "rem": "rem_(re:zero)",
            "ruby": "kurosawa_ruby",
            "ruka": "sarashina_ruka",
            "senko": "senko_(sewayaki_kitsune_no_senko-san)",
            "shiro": "shiro_(sewayaki_kitsune_no_senko-san)",
            "sumi": "sakurasawa_sumi",
            "unicorn": "unicorn_(azur_lane)",
            "you": "watanabe_you",
            "zero_two": "zero_two_(darling_in_the_franxx)",
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or self.site_name != "danbooru":
            return

        ctx = await self.bot.get_context(message)
        if ctx.command is not None or ctx.prefix is None:
            return

        args = ctx.message.content[len(ctx.prefix):].split(" ")
        # try:
        #     shortcut = self.shortcuts.get(args[:args.index(" ")], None)
        #     args = args[args.index(" ")+1:]
        # except:
        #     shortcut = self.shortcuts.get(args, None)
        #     args = ""

        if not shortcut:
            return

        try:
            if (not isinstance(ctx.channel, discord.DMChannel)
                    and not ctx.channel.is_nsfw()):
                raise commands.errors.NSFWChannelRequired(ctx.channel)

            await self.booru(ctx, tags=shortcut + " " + args)
        except commands.errors.NSFWChannelRequired as err:
            #! should handle the errors with the default on_command_error
            await ctx.send(err)
            return

    @commands.command(aliases=["shortcuts"])
    async def waifus(self, ctx):
        longestKey = max(len(k) for k in self.shortcuts.keys())
        shortcuts = "**Available shortcuts:**```"
        for k in sorted(self.shortcuts):
            shortcut = f"\n{k}:" + ' ' * \
                (longestKey - len(k) + 1) + self.shortcuts[k]
            if len(shortcuts) + len(shortcut) > 2000-3:
                await ctx.send(shortcuts + "```")
                shortcuts = "```" + shortcut
            else:
                shortcuts += shortcut

        await ctx.send(f"{shortcuts}```You can add your waifus using xd addshortcut :)")

    @commands.cooldown(5, 3600.0, commands.BucketType.user)
    @commands.command()
    async def addshortcut(self, ctx, key, danbooruTags):
        """add a shortcut for your waifu. 1 hour cooldown after 5 calls, so use it carefully"""
        if self.shortcuts.get(key, None):
            await ctx.send("There is already a shortcut with that key!")
        elif self.bot.get_command(key):
            await ctx.send("You can't name a shortcut with the name of a command!")
        elif len(key) > 20:
            await ctx.send("The key is too long, make it shorter")
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

    @commands.is_owner()
    @commands.command(hidden=True)
    async def togglensfw(self, ctx):
        global clovisProtection
        clovisProtection = not clovisProtection
        if clovisProtection:
            await ctx.message.add_reaction("✅")
        else:
            await ctx.message.add_reaction("❎")

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
        start = time.time()
        await self.booru(ctx, tags=tags)
        end = time.time() - start
        print(end)


class Safebooru(BooruCog, name="Booru"):
    @commands.is_nsfw()
    @commands.command(aliases=["safe"])
    async def safebooru(self, ctx, *, tags="rating:s"):
        """Wow searching on safebooru that's so original"""
        await self.booru(ctx, tags=tags)


def setup(bot: commands.Bot):
    bot.add_cog(DanbooruCog(bot))
    bot.add_cog(Yandere(bot, Moebooru, "yandere",
                        "https://yande.re/post/show/"))
    bot.add_cog(Konachan(bot, Moebooru, "konachan",
                         "https://konachan.com/post/show/"))
    bot.add_cog(Safebooru(bot, Danbooru, "safebooru",
                          "https://safebooru.donmai.us/posts/"))
