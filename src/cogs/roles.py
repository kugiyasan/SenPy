import discord
from discord.ext import commands
import asyncio
from enum import Enum
from typing import List

from .utils.dbms import db


class RoleActions(Enum):
    ADD = 1
    DEL = 2
    MANAGEADD = 3
    MANAGEDEL = 4


class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(aliases=["addRole"])
    async def addrole(self, ctx: commands.Context):
        """give yourself a certain role in the server"""
        await self.roleEmbed(ctx, RoleActions.ADD)

    @commands.guild_only()
    @commands.command(
        aliases=["delRole", "deleteRole", "deleterole", "removeRole", "removerole"]
    )
    async def delrole(self, ctx: commands.Context):
        """Remove roles from yourself"""
        await self.roleEmbed(ctx, RoleActions.DEL)

    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def manageaddrole(self, ctx: commands.Context):
        """Admin command. Let you choose which roles can be given by the bot"""
        await self.roleEmbed(ctx, RoleActions.MANAGEADD)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def managedelrole(self, ctx: commands.Context):
        """Admin command. Let you choose which roles can be given by the bot"""
        await self.roleEmbed(ctx, RoleActions.MANAGEDEL)

    @staticmethod
    def renderEmbed(roles: List[discord.Role], page: int):
        title = (
            "React to the number associated with the role you want to interact with!"
        )

        description = []
        for n in range(9):
            try:
                role = roles[9 * page + n]
            except IndexError:
                break

            description.append(f"{n+1}\ufe0f\u20e3: {role}")

        embed = discord.Embed(
            title=title,
            description="\n".join(description),
            colour=discord.Colour.gold(),
        )
        embed.set_footer(text=f"Page {page+1}")

        return embed

    def getUserAvailableRoles(
        self,
        authorRoles: List[discord.Role],
        guild: discord.Guild,
        roleAction: RoleActions,
    ) -> List[discord.Role]:
        command = "SELECT rolesToGive FROM guilds WHERE id=%s"
        try:
            roles = db.get_data(command, (guild.id,))[0][0] or []
        except TypeError:
            roles = []

        if roleAction == RoleActions.ADD:
            roles = set(roles).difference(role.id for role in authorRoles)
        elif roleAction == RoleActions.DEL:
            roles = set(roles).intersection(role.id for role in authorRoles)
        elif roleAction == RoleActions.MANAGEADD:
            roles = set(
                role.id
                for role in guild.roles
                if not role.managed and not role.is_default()
            ).difference(roles)

        # TODO should clean the database here if there is some dangling roles
        roles = (guild.get_role(role) for role in roles)
        roles = (role for role in roles if role is not None)
        return sorted(roles, key=lambda e: e.name)

    async def initEmbed(
        self, ctx: commands.Context, roleAction: RoleActions, page: int
    ):
        if isinstance(ctx.author, discord.User) or not ctx.guild:
            return
        roles = self.getUserAvailableRoles(ctx.author.roles, ctx.guild, roleAction)

        if not len(roles):
            return None, None

        message = await ctx.send(embed=self.renderEmbed(roles, page))

        if len(roles) <= 9:
            for n in range(9):
                # Add number emoji
                await message.add_reaction(f"{n+1}\ufe0f\u20e3")
        else:
            await message.add_reaction("◀")
            await message.add_reaction("▶")
            for n in range(9):
                # Add number emoji from 1 to 9 inclusive
                await message.add_reaction(f"{n+1}\ufe0f\u20e3")

        return roles, message

    async def roleEmbed(self, ctx: commands.Context, roleAction: RoleActions) -> None:
        page = 0
        roles, message = await self.initEmbed(ctx, roleAction, page)

        if roles is None or message is None:
            await ctx.send("There's no available role! Exiting...")
            return

        emoji = ""

        def check(reaction, member):
            return ctx.author == member and reaction.message.id == message.id

        while True:
            if emoji == "◀":
                page -= 1
            elif emoji == "▶":
                page += 1
            elif emoji.endswith("\ufe0f\u20e3"):
                # if a emoji with a number is pressed
                if emoji[0] != "0":
                    await message.clear_reactions()
                    roleNumber = 9 * page - 1 + int(emoji[0])
                    await self.numberEmojiSelected(ctx, roleNumber, roles, roleAction)
                    return

            page %= (len(roles) - 1) // 9 + 1
            await message.edit(embed=self.renderEmbed(roles, page))

            try:
                res = await self.bot.wait_for("reaction_add", check=check, timeout=30)
            except asyncio.TimeoutError:
                await message.clear_reactions()
                return

            emoji = str(res[0].emoji)
            await message.remove_reaction(res[0].emoji, res[1])

    async def numberEmojiSelected(
        self,
        ctx: commands.Context,
        roleNumber: int,
        roles: List[discord.Role],
        roleAction: RoleActions,
    ):
        # TODO The user shouldn't see None anymore
        if roleNumber >= len(roles):
            await ctx.send("You chose None! Exiting...")
            return

        role = roles[roleNumber]
        if isinstance(ctx.author, discord.User) or not ctx.guild:
            return
        author = ctx.author

        if roleAction == RoleActions.ADD:
            await author.add_roles(role, reason="senpy addrole")
            await ctx.send(f"You chose : {role.name}! The role is added!")
        elif roleAction == RoleActions.DEL:
            await author.remove_roles(role, reason="senpy delrole")
            await ctx.send(f"You chose : {role.name}! The role is removed!")
        elif roleAction == RoleActions.MANAGEADD:
            db.set_data(
                """INSERT INTO guilds (id, rolesToGive)
                    VALUES (%s, Array [%s])
                    ON CONFLICT(id)
                    DO UPDATE SET rolesToGive=guilds.rolesToGive||%s""",
                (ctx.guild.id, role.id, role.id),
            )

            await ctx.send(f"{role.name} is now available for the members!")
        elif roleAction == RoleActions.MANAGEDEL:
            db.set_data(
                "UPDATE guilds SET rolesToGive=array_remove(rolesToGive, %s)",
                (role.id,),
            )

            await ctx.send(f"{role.name} is now unavailable for the members!")


def setup(bot: commands.Bot):
    bot.add_cog(Roles(bot))
