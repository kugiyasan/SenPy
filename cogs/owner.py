import discord
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        pass

def setup(bot):
    bot.add_cog(Greetings(bot))