import discord
from discord.ext import commands

from cogs.utils.dbms import conn


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(hidden=True)
    async def activity(self, ctx, *, string):
        occupation = discord.Activity(
            type=discord.ActivityType.playing, name=string)
        await self.bot.change_presence(activity=occupation)

    @commands.command()
    async def ban(self, ctx, member: discord.Member):
        """wait the bot has ban permission?!?"""
        await ctx.send(f"""`{member.name} has been banned from the server...\njust kidding I can\'t do that`""")

    @commands.command(aliases=['purge', 'del'])
    async def delete(self, ctx: commands.Context, count: int = 1):
        """delete the last messages of the bot"""
        await ctx.message.delete()
        n = 0

        async for message in ctx.history(limit=100):
            if message.author == self.bot.user:
                await message.delete()
                n += 1

                if n == count:
                    break

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx: commands.Context, newPrefix):
        """change the command prefix for this server"""
        if len(newPrefix) > 4:
            await ctx.send('The new prefix is too long, can you make it shorter please?')
            return

        with conn:
            conn.execute("UPDATE guilds SET command_prefix = ? WHERE id = ?", (newPrefix, ctx.guild.id))

        await ctx.send(f'The new command prefix for this server is "{newPrefix}"')


def setup(bot):
    bot.add_cog(Admin(bot))
