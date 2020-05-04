import discord
from discord.ext import commands

from pathlib import Path
import git
import json

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx, *members: discord.Member):
        """wait the bot has ban permission?!?"""
        output = ', '.join(m.name for m in members)
        await ctx.send(f'''`{output} has been banned from the server...\njust kidding I can\'t do that`''')

    @commands.command()
    async def delete(self, ctx: commands.Context, count: int=1):
        """delete the last message of the bot"""
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

    @commands.command()
    async def addrole(self, ctx: commands.Context, *roles):
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
        with open('config.json', 'r') as configFile:
            j = json.load(configFile)

        for guild in j['guilds']:
            if guild['name'] == ctx.guild.name:
                guild['command_prefix'] = newPrefix
                break
        else:
            j['guilds'].append({"name": ctx.guild.name,
                                "command_prefix": newPrefix})

        with open('config.json', 'w+') as configFile:
            json.dump(j, configFile)

        await ctx.send(f'The new command prefix for this server is "{newPrefix}"')

def setup(bot):
    bot.add_cog(Admin(bot))