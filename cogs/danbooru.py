import discord
from discord.ext import commands

from pybooru import Danbooru
import random
import requests
from cogs.utils.sendEmbed import sendEmbed
from cogs.mofupoints import incrementEmbedCounter


class DanbooruCog(commands.Cog, name="Danbooru"):
    def __init__(self, bot):
        self.bot = bot
        self.urlsTags = {}
        self.client = Danbooru("danbooru")
        self.clovisProtection = True
        self.shortcuts = {
            "unicorn": "unicorn_(azur_lane)",
            "rem": "rem_(re:zero)",
            "emilia": "emilia_(re:zero)",
            "hanamaru": "kunikida_hanamaru",
            "maru": "kunikida_hanamaru",
            "zero_two": "zero_two_(darling_in_the_franxx)",
            "02": "zero_two_(darling_in_the_franxx)",
            "megumin": "megumin",
            "ruka": "sarashina_ruka",
            "sumi": "sakurasawa_sumi",
            "chika": "fujiwara_chika",
            "shiro": "shiro_(sewayaki_kitsune_no_senko-san)",
            "you": "watanabe_you",
            "ruby": "kurosawa_ruby",
            "korone": "inugami_korone",
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        ctx = await self.bot.get_context(message)
        if ctx.command is None and ctx.prefix is not None:
            key = ctx.message.content[len(ctx.prefix):]
            tags = self.shortcuts.get(key, None)

            if tags:
                try:
                    if not ctx.channel.is_nsfw():
                        raise commands.errors.NSFWChannelRequired(ctx.channel)

                    await self.danbooru(ctx, tags=tags)
                except commands.errors.NSFWChannelRequired as err:
                    #! should handle the errors with the default on_command_error
                    await ctx.send(err)
                    return

    @commands.command()
    async def waifus(self, ctx):
        longestKey = max(len(k) for k in self.shortcuts.keys())
        shortcuts = "**Available shortcuts:**```"
        for k, v in self.shortcuts.items():
            shortcut = f"\n{k}:" + ' ' * (longestKey - len(k) + 1) + v
            if len(shortcuts) + len(shortcut) > 2000-3:
                await ctx.send(shortcuts + "```")
                shortcuts = "```" + shortcut
            else:
                shortcuts += shortcut

        await ctx.send(f"{shortcuts}```You can add your waifus using xd addshortcut :)")

    @commands.cooldown(5, 3600.0, commands.BucketType.user)
    @commands.command()
    async def addshortcut(self, ctx, key, danbooruTags):
        """add a shortcut for your waifu. 1 hour cooldown, so use it carefully"""
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
        self.clovisProtection = not self.clovisProtection
        if self.clovisProtection:
            await ctx.message.add_reaction("✅")
        else:
            await ctx.message.add_reaction("❎")

    @commands.is_nsfw()
    @commands.command(aliases=["db", "dan"])
    async def danbooru(self, ctx: commands.Context, *, tags="rating:s"):
        """Wow searching on danbooru that's so original"""
        if not len(self.urlsTags.get(tags, {})):
            await self.requestDanbooru(tags)

            if not len(self.urlsTags.get(tags, {})):
                await ctx.send("I couldn't find any image with that tag!")
                return

        post = self.urlsTags[tags].pop()
        if post["rating"] != "s" and not ctx.channel.is_nsfw():
            raise commands.errors.NSFWChannelRequired(ctx.channel)

        if ctx.author.id == 276038064273489930 and self.clovisProtection == True:
            if "rating:e" in tags:
                await ctx.send("I couldn't find any image with that tag!")
                return

            while post["rating"] == "e":
                print(f"dropping {post}")
                post = self.urlsTags[tags].pop()

        await ctx.send(embed=self.danbooruEmbed(post))
        await incrementEmbedCounter(ctx.author)

    async def requestDanbooru(self, tags):
        print("resquesting danbooru")

        posts = self.client.post_list(tags=tags, limit=100, random=True)

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
        post_url = f"https://danbooru.donmai.us/posts/{post['id']}"
        print(post_url)
        embed = discord.Embed(
            color=discord.Colour.gold(),
            title=f"sauce",
            url=post_url
        )

        embed.set_image(url=post["file_url"])
        embed.set_author(name=post["tag_string_artist"])
        embed.set_footer(text=f'{post["score"]}⬆️')

        return embed


def setup(bot: commands.Bot):
    bot.add_cog(DanbooruCog(bot))
