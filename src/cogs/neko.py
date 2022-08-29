from discord.ext import commands

import nekos
import random
import re

from .utils.sendEmbed import sendEmbed
from .utils.deleteMessage import deleteMessage


def get_owo(text: str) -> str:
    # https://github.com/Nekos-life/neko-website/blob/78b2532de2d91375d6de45e4446fc766ba169472/app.py#L78
    # This function is stupidly simple, but I'm too lazy to write it myself
    faces = ["owo", "UwU", ">w<", "^w^"]
    v = text
    r = re.sub("[rl]", "w", v)
    r = re.sub("[RL]", "W", r)
    r = re.sub("ove", "uv", r)
    r = re.sub("n", "ny", r)
    r = re.sub("N", "NY", r)
    r = re.sub("[!]", " " + random.choice(faces) + " ", r)
    return r


class Neko(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.is_nsfw()
    @commands.command()
    async def neko(self, ctx: commands.Context, style: str = "neko") -> None:
        """Send some cute nekos on your server!"""
        try:
            await sendEmbed(ctx, nekos.img(style))
        except nekos.InvalidArgument as err:
            await ctx.send(err)

    @commands.command()
    async def fact(self, ctx: commands.Context) -> None:
        """Get yo facts right!"""
        await deleteMessage(ctx)
        await ctx.send(nekos.fact())

    @commands.command()
    async def owo(self, ctx: commands.Context, *, text: str) -> None:
        """yay cute wwitinyg >w<"""
        text = text or "give me a text to owoify!"
        await deleteMessage(ctx)
        await ctx.send(get_owo(text))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Neko(bot))
