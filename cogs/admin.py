import discord
from discord.ext import commands

from pathlib import Path
import git
import json

from cogs.utils.configJson import updateValueJson

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx, *members: discord.Member):
        """wait the bot has ban permission?!?"""
        output = ', '.join(m.name for m in members)
        await ctx.send(f'''`{output} has been banned from the server...\njust kidding I can\'t do that`''')

    @commands.command(aliases=['purge', 'del'])
    async def delete(self, ctx: commands.Context, count: int=1):
        """delete the last messages of the bot"""
        await ctx.message.delete()
        n = 0

        async for message in ctx.history():
            if message.author == self.bot.user:
                await message.delete()
                n += 1

                if n == count:
                    break

    @commands.command(hidden=True)
    @commands.is_owner()
    async def gitpull(self, ctx: commands.Context):
        g = git.cmd.Git(Path(__file__).resolve().parent)
        g.pull()

    @commands.command(aliases=['role', 'getrole'])
    async def addrole(self, ctx: commands.Context, *roles):
        '''give yourself a certain role in the server'''
        output = []

        for role in ctx.guild.roles:
            if role.name in roles:
                await ctx.author.add_roles(role, reason='Get a life instead of reading logs')
                output.append(role.name)
        string = ', '.join(output)
        if not string:
            await ctx.send('No role added, be sure to give me the exact role name')
            return
        await ctx.send(f'Done! You are now in the {string} gang!')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx: commands.Context, newPrefix):
        '''change the command prefix for this server'''
        await updateValueJson(newPrefix, ctx.guild.name, 'command_prefix')

        await ctx.send(f'The new command prefix for this server is "{newPrefix}"')

    @commands.command(aliases=['rule'])
    async def rules(self, ctx: commands.Context):
        '''Send the server's rules'''
        if ctx.guild.id == 509558996399816732:
            await ctx.send("Common rule: Do support t-series or you'll get banned")
        else:
            output = []
            # rules_channel = ctx.guild.rules_channel
            for channel in ctx.guild.channels:
                if 'rule' in channel.name.lower():
                    rules_channel = channel
                    break

            if not rules_channel:
                await ctx.send('No rules on this server, FFA bois')

            async for msg in rules_channel.history():
                output.append(msg.content)
            await ctx.send('\n'.join(output[::-1]))


def setup(bot):
    bot.add_cog(Admin(bot))