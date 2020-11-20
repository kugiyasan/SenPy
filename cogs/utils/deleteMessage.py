import discord


async def deleteMessage(ctx):
    # so ctx is a bad name for the variable, I know
    if not isinstance(ctx, discord.Message):
        ctx = ctx.message

    try:
        await ctx.delete()
    except discord.Forbidden:
        pass
