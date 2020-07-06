import discord

# from cogs.utils.dbms import
from cogs.mofupoints import incrementEmbedCounter


async def sendEmbed(ctx, url, localImageFile=None, **kwargs):
    print(url)

    await incrementEmbedCounter(ctx.author)

    if localImageFile:
        embed = discord.Embed(
            color=discord.Colour.gold(),
            **kwargs)
    else:
        embed = discord.Embed(
            type='image',
            color=discord.Colour.gold(),
            **kwargs)

    embed.set_image(url=url)

    try:
        await ctx.send(embed=embed, file=localImageFile)
    except:
        await ctx.send(url, file=localImageFile)
