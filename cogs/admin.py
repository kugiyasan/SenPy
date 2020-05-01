import discord
from discord.ext import commands

from pathlib import Path
import git

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx, *members: discord.Member):
        """wait the bot has ban permission?!?"""
        output = ', '.join(m.name for m in members)
        await ctx.send(f'''`{output} has been banned from the server...\njust kidding I can\'t do that`''')

    @commands.command()
    async def delete(self, ctx: commands.Context):
        """delete the last message of the bot"""
        await ctx.message.delete()

        async for message in ctx.history():
            if message.author == self.bot.user:
                await message.delete()
                break

    @commands.command(hidden=True)
    @commands.is_owner()
    async def gitpull(self, ctx: commands.Context):
        g = git.cmd.Git(Path(__file__).resolve().parent)
        g.pull()




def setup(bot):
    bot.add_cog(Admin(bot))