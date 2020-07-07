import discord

from cogs.mofupoints import incrementEmbedCounter


async def sendEmbed(ctx, url, localImageFile=None, **kwargs):
    print(url)

    if hasattr(ctx, 'author'):
        await incrementEmbedCounter(ctx.author)

    embed = discord.Embed(
        color=discord.Colour.gold(),
        **kwargs)

    embed.set_image(url=url)

    try:
        await ctx.send(embed=embed, file=localImageFile)
    except:
        await ctx.send(url, file=localImageFile)
