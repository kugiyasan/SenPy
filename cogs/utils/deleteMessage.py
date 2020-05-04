import discord

async def deleteMessage(ctx):
    if type(ctx) == discord.Message: # so ctx is a bad name for the variable, I know
        try:
            await ctx.delete()
        except:
            pass
    try:
        await ctx.message.delete()
    except:
        pass