import discord
from discord.ext import commands

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fasterImg(self, ctx):
        pass

    # @commands.command(name='spam', hidden=True)
    # async def _spam(self, ctx, times: int = 1, *, msg: str = 'spam'):
    #     """ Repeat a message multiple times.
    #     """
    #     for i in range(times):
    #         await ctx.send(msg)

    @commands.command()
    async def beautifulMessage(self, ctx):
        # image = discord.File(open('../senko-san.jpg', 'rb'))
        await ctx.send(embed=discord.Embed(
            title='Hello World',
            description='test test',
            url='https://i.redd.it/lr3cj0w4f3x31.jpg',
            set_footer='mofu mofu!',
            set_image='https://i.redd.it/lr3cj0w4f3x31.jpg',
            set_thumbnail='https://i.redd.it/lr3cj0w4f3x31.jpg',
            color=discord.Colour.gold()))

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

def setup(bot):
    bot.add_cog(Dev(bot))