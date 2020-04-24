import discord
from discord.ext import commands

class Basics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(name='spam', hidden=True)
    # async def _spam(self, ctx, times: int = 1, *, msg: str = 'spam'):
    #     """ Repeat a message multiple times.
    #     """
    #     for i in range(times):
    #         await ctx.send(msg)

    @commands.command()
    async def ban(self, ctx, *members: discord.Member):
        """wait the bot has ban permission?!?"""
        output = ', '.join(m.name for m in members)
        await ctx.send(f'`{output} has been banned from the server... just kidding I can\'t do that`')

    @commands.command()
    async def delete(self, ctx: commands.Context):
        """delete the last message of the bot"""
        await ctx.message.delete()
        async for message in ctx.history():
            if message.author.bot:
                await message.delete()
                break

    # @commands.command(name='kick')
    # @commands.is_owner()
    # # @commands.has_permissions(kick_members=True)
    # @commands.guild_only()
    # async def _kick(self, ctx, *members: discord.Member):
    #     """ Kicks the specified member(s).
    #     """
    #     for member in members:
    #         await ctx.message.guild.kick(member)
    #         await ctx.send(f'```{member} was kicked from the server.```')

    @commands.command()
    async def ping(self, ctx):
        ping =  round(self.bot.latency * 1000)
        await ctx.send(f"Pong! My ping is {ping}ms")

def setup(bot):
    bot.add_cog(Basics(bot))