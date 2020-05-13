import discord
from discord.ext import commands

async def sendEmbed(ctx, url, **kwargs):
    print(url)
    e = discord.Embed(
        type='image',
        color=discord.Colour.gold(),
        **kwargs)
    e.set_image(url=url)

    try:
        await ctx.send(embed=e)
    except:
        await ctx.send(url)