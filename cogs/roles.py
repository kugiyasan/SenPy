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
        await self.roleEmbed(ctx, RoleActions.ADD)

    @commands.guild_only()
    @commands.command(aliases=["delRole", "deleteRole", "deleterole", "removeRole", "removerole"])
    async def delrole(self, ctx: commands.Context):
        await self.roleEmbed(ctx, RoleActions.DEL)

    async def getRoles(self, guildid):
        with conn:
            cursor.execute(
                "SELECT rolesToGive FROM guilds WHERE id=%s", (guildid,))
            roles = cursor.fetchone()[0]
        return roles

    async def renderEmbed(self, ctx, roles, page):
        title = "React to the number associated with the role you want!"

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
        roles = await self.getRoles(ctx.guild.id)
        if roleAction == RoleActions.DEL:
            roles = set(roles).intersection(
                role.id for role in ctx.author.roles)

        roles = [ctx.guild.get_role(role) for role in roles]

        page = 0

        message = await ctx.send(embed=await self.renderEmbed(ctx, roles, page))
        await message.add_reaction("◀")
        await message.add_reaction("▶")
        for n in range(1, 10):
            await message.add_reaction(f"{n}\ufe0f\u20e3")

        emoji = ""

        def check(reaction, member):
            return ctx.author == member

        while True:
            if emoji == "◀":
                page -= 1
            elif emoji == "▶":
                page += 1
            elif emoji.endswith("\ufe0f\u20e3"):
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

                await message.clear_reactions()
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


def setup(bot):
    bot.add_cog(Roles(bot))
