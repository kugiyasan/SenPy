import discord

# from cogs.utils.configJson import 
from cogs.mofupoints import incrementEmbedCounter

async def sendEmbed(ctx, url, **kwargs):
    print(url)

    await incrementEmbedCounter(ctx.author)

    e = discord.Embed(
        type='image',
        color=discord.Colour.gold(),
        **kwargs)
    e.set_image(url=url)

    try:
        await ctx.send(embed=e)
    except:
        await ctx.send(url)