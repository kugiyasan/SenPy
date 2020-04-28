import discord
from discord.ext import commands

async def sendEmbed(ctx, url):
    print(url)
    e = discord.Embed(
        type='image',
        color=discord.Colour.gold())
    e.set_image(url=url)
    await ctx.send(embed=e)