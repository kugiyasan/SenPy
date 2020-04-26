import discord

async def deleteMessage(ctx):
    try:
        await ctx.message.delete()
    except:
        pass