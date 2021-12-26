from typing import Any
import discord
from discord.ext import commands

from ..mofupoints import incrementEmbedCounter


async def sendEmbed(
    ctx: commands.Context, url: str, localImageFile: discord.File = None, **kwargs: Any
) -> None:
    print(url)

    if hasattr(ctx, "author"):
        incrementEmbedCounter(ctx.author)

    embed = discord.Embed(color=discord.Colour.gold(), **kwargs)

    embed.set_image(url=url)

    try:
        await ctx.send(embed=embed, file=localImageFile)
    except discord.Forbidden:  # we don't have permission to send embed
        await ctx.send(url, file=localImageFile)
