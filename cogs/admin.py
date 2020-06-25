import discord
from discord.ext import commands

from cogs.utils.configJson import getValueJson, updateValueJson

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx, member: discord.Member):
        """wait the bot has ban permission?!?"""
        await ctx.send(f'''`{member.name} has been banned from the server...\njust kidding I can\'t do that`''')

    @commands.command(aliases=['purge', 'del'])
    async def delete(self, ctx: commands.Context, count: int=1):
        """delete the last messages of the bot"""
        await ctx.message.delete()
        n = 0

        async for message in ctx.history(limit=100):
            if message.author == self.bot.user:
                await message.delete()
                n += 1

                if n == count:
                    break

    @commands.command(aliases=['getrole'])
    async def addrole(self, ctx: commands.Context, *roles):
        '''give yourself a certain role in the server'''
        await self.role(ctx, action='add', *roles)

    @commands.command(aliases=['removerole', 'deleterole', 'rmrole'])
    async def delrole(self, ctx: commands.Context, *roles):
        '''Remove roles from yourself'''
        await self.role(ctx, action='remove', *roles)

    @commands.command()
    async def role(self, ctx, action='add', *roles):
        roleToUpdate = []
        availableRoles = await getValueJson('guilds', ctx.guild.name, 'rolesToGive')

        for role in ctx.guild.roles:
            if (role.name in roles
                and role.name in availableRoles):
                roleToUpdate.append(role)

        string = ', '.join(role.name for role in roleToUpdate)
        if not string:
            await ctx.send('No role updated, be sure to give me the exact role name')
            return

        if action == 'add':
            await ctx.author.add_roles(*roleToUpdate, reason='xd addrole')
            await ctx.send(f'Done! You are now in the {string} gang!')
        elif action == 'remove':
            await ctx.author.remove_roles(*roleToUpdate, reason='xd rmrole')
            await ctx.send(f'You left the {string} gang')
        else:
            await ctx.send('Unknown action. Usage: `xd role add|remove *roles*`')
            return

    @commands.command()
    async def roles(self, ctx):
        '''Emumerate every role that you can give yourself on this server'''
        roles = await getValueJson('guilds', ctx.guild.name, 'rolesToGive')

        if not roles:
            await ctx.send('There is no role that I can give!')
            return

        await ctx.send('Available roles: ' + ', '.join(roles))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def manageRoles(self, ctx, action, *newroles):
        if action == 'add':
            roles = await getValueJson('guilds', ctx.guild.name, 'rolesToGive', default=[])

            confirmedRoles = []
            for role in ctx.guild.roles:
                if role.name in newroles:
                    confirmedRoles.append(role.name)

            if not roles:
                updatedRoles = list(set(confirmedRoles))
            else:
                updatedRoles = list(set(confirmedRoles).update(roles))

            await updateValueJson(updatedRoles, 'guilds', ctx.guild.name, 'rolesToGive')
            await ctx.send(f"Role(s) that I can now give: {' '.join(updatedRoles)}")

        elif action == 'remove':
            roles = await getValueJson('guilds', ctx.guild.name, 'rolesToGive')

            if not roles:
                await ctx.send('No role to remove!')
                return
            else:
                updatedRoles = set(roles).difference_update(newroles)
                if not updatedRoles:
                    await updateValueJson([], 'guilds', ctx.guild.name, 'rolesToGive')
                    await ctx.send("I can't give roles now!")
                    return

            await updateValueJson(list(updatedRoles), 'guilds', ctx.guild.name, 'rolesToGive')
            await ctx.send(f"Role(s) that I can now give: {' '.join(updatedRoles)}")

        else:
            await ctx.send('Unknown action. Usage: "xd manageRoles add|remove *roles*"')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx: commands.Context, newPrefix):
        '''change the command prefix for this server'''
        if len(newPrefix) > 4:
            await ctx.send('The new prefix is too long, can you make it shorter please?')
            return

        await updateValueJson(newPrefix, 'guilds', ctx.guild.name, 'command_prefix')

        await ctx.send(f'The new command prefix for this server is "{newPrefix}"')


def setup(bot):
    bot.add_cog(Admin(bot))