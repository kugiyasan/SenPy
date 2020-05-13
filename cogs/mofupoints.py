import discord
from discord.ext import commands

class MofuPoints(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['top'])
    async def leaderboard(self, ctx, *, member: discord.Member = None):
        """Show the leaderboard for the top fluffer"""
        pass

def setup(bot):
    bot.add_cog(MofuPoints(bot))