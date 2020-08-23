import discord
from discord.ext import commands
import asyncio
from enum import Enum

from cogs.utils.dbms import conn, cursor


class RoleActions(Enum):
    ADD = 1
    DEL = 2
    MANAGEADD = 3
    MANAGEDEL = 4


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(aliases=["addRole"])
    async def addrole(self, ctx: commands.Context):
        """give yourself a certain role in the server"""
        await self.roleEmbed(ctx, RoleActions.ADD)

    @commands.guild_only()
    @commands.command(aliases=["delRole", "deleteRole", "deleterole", "removeRole", "removerole"])
    async def delrole(self, ctx: commands.Context):
        """Remove roles from yourself"""
        await self.roleEmbed(ctx, RoleActions.DEL)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def manageaddrole(self, ctx: commands.Context):
        """Admin command. Let you choose which roles can be given by the bot"""
        ch = ctx.channel
        permissions = ch.permissions_for(ctx.author)

        if permissions.manage_roles == False:
            await ctx.send("Give me the manage_roles permissions if you want me to give roles!")
            return

        await self.roleEmbed(ctx, RoleActions.MANAGEADD)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def managedelrole(self, ctx: commands.Context):
        """Admin command. Let you choose which roles can be given by the bot"""
        await self.roleEmbed(ctx, RoleActions.MANAGEDEL)

    async def renderEmbed(self, ctx, roles, page):
        title = "React to the number associated with the role you want to interact with!"

        description = []
        for n in range(1, 10):
            role = None
            if 9*page+n-1 < len(roles):
                role = roles[9*page+n-1]

            description.append(f"{n}\ufe0f\u20e3: {role}")

        description = "\n".join(description)

        embed = discord.Embed(
            title=title,
            description=description,
            colour=discord.Colour.gold()
        )
        embed.set_footer(text=f"Page {page+1}")

        return embed

    async def roleEmbed(self, ctx: commands.Context, roleAction):
        with conn:
            cursor.execute(
                "SELECT rolesToGive FROM guilds WHERE id=%s", (ctx.guild.id,))
            try:
                roles = cursor.fetchone()[0]
            except:
                roles = []

        if roleAction == RoleActions.ADD:
            roles = set(roles).difference(
                role.id for role in ctx.author.roles)
        elif roleAction == RoleActions.DEL:
            roles = set(roles).intersection(
                role.id for role in ctx.author.roles)
        elif roleAction == RoleActions.MANAGEADD:
            roles = set(role.id for role in ctx.guild.roles if not role.managed and not role.is_default(
            )).difference(roles)

        roles = [ctx.guild.get_role(role) for role in roles]

        if not len(roles):
            await ctx.send("There isn't an available role! Exiting...")
            return

        page = 0

        message = await ctx.send(embed=await self.renderEmbed(ctx, roles, page))
        await message.add_reaction("◀")
        await message.add_reaction("▶")
        for n in range(1, 10):
            await message.add_reaction(f"{n}\ufe0f\u20e3")

        emoji = ""

        def check(reaction, member):
            return (ctx.author == member
                    and reaction.message.id == message.id)

        while True:
            if emoji == "◀":
                page -= 1
            elif emoji == "▶":
                page += 1
            elif emoji.endswith("\ufe0f\u20e3"):
                # if a emoji with a number is pressed
                if emoji[0] != "0":
                    await self.numberEmojiSelected(ctx, message, emoji, page, roles, roleAction)
                    return

            page %= (len(roles)-1) // 9 + 1
            await message.edit(embed=await self.renderEmbed(ctx, roles, page))

            try:
                res = await self.bot.wait_for("reaction_add", check=check, timeout=30)
            except asyncio.exceptions.TimeoutError:
                await message.clear_reactions()
                return

            emoji = str(res[0].emoji)
            await message.remove_reaction(res[0].emoji, res[1])

    async def numberEmojiSelected(self, ctx, message, emoji, page, roles, roleAction):
        roleNumber = 9*page-1+int(emoji[0])
        if roleNumber >= len(roles):
            await ctx.send("You chose None! Exiting...")
            await message.clear_reactions()
            return

        role = roles[roleNumber]

        if roleAction == RoleActions.ADD:
            await ctx.author.add_roles(role, reason="xd addrole")
            await ctx.send(f"You chose : {role.name}! The role is added!")
        elif roleAction == RoleActions.DEL:
            await ctx.author.remove_roles(role, reason="xd delrole")
            await ctx.send(f"You chose : {role.name}! The role is removed!")
        elif roleAction == RoleActions.MANAGEADD:
            with conn:
                cursor.execute(
                    """INSERT INTO guilds (id, rolesToGive)
                        VALUES (%s, Array [%s])
                        ON CONFLICT(id)
                        DO UPDATE SET rolesToGive=guilds.rolesToGive||%s""", (ctx.guild.id, role.id, role.id))

            await ctx.send(f"{role.name} is now available for the users!")
        elif roleAction == RoleActions.MANAGEDEL:
            with conn:
                cursor.execute(
                    "SELECT rolesToGive FROM guilds WHERE id=%s", (ctx.guild.id,))
                newRoles = cursor.fetchone()[0]
                newRoles.remove(role.id)

                if not len(newRoles):
                    cursor.execute(
                        "UPDATE guilds SET rolesToGive=ARRAY[]::BIGINT[] WHERE id=%s", (ctx.guild.id,))
                else:
                    cursor.execute(
                        "UPDATE guilds SET rolesToGive=%s WHERE id=%s", (newRoles, ctx.guild.id))

            await ctx.send(f"{role.name} is now unavailable for the users!")

        await message.clear_reactions()


def setup(bot: commands.Bot):
    bot.add_cog(Roles(bot))
