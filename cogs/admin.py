import discord
from discord.ext import commands

from cogs.utils.deleteMessage import deleteMessage
from cogs.utils.dbms import conn, cursor


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(hidden=True)
    async def activity(self, ctx, *, string):
        occupation = discord.Activity(
            type=discord.ActivityType.playing, name=string)
        await self.bot.change_presence(activity=occupation)

    @commands.command(aliases=['purge', 'del'])
    async def delete(self, ctx: commands.Context, count: int = 1):
        """delete the last messages of the bot"""
        await deleteMessage(ctx)
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
        with conn:
            cursor.execute("""INSERT INTO guilds (id, command_prefix)
                            VALUES(%s, %s) 
                            ON CONFLICT(id) 
                            DO UPDATE SET command_prefix = %s""", (ctx.guild.id, newPrefix, newPrefix))

        await ctx.send(f'The new command prefix for this server is "{newPrefix}"')


def setup(bot):
    bot.add_cog(Admin(bot))
