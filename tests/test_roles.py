import discord
from discord.ext import commands
import discord.ext.test as dpytest
import pytest
from typing import List

# TODO addrole, delrole, manageaddrole, managedelrole
# addrole:
#   when len(roles) == 0
#   when len(roles) == 1
#   when len(roles) > 10


class State:
    http = None


async def create_random_roles(guild: discord.Guild) -> List[discord.Role]:
    names = (
        "Red",
        "Green",
        "Blue",
        "Orange",
        "Yellow",
        "Purple",
        "Owner",
        "Member",
        "A Random Role",
        "I don't have ideas anymore",
    )
    roles = []

    for i in range(len(names)):
        data = {"id": i, "name": names[i]}
        role = discord.Role(guild=guild, state=State(), data=data)
        roles.append(role)
        await dpytest.create_role_callback(guild, role)

    return roles


# @pytest.mark.asyncio
# async def test_addrole(bot, prefix):
#     await create_random_roles(bot.guilds[0])
#     await dpytest.message(f"{prefix} addrole")


@pytest.mark.asyncio
async def test_manageaddrole(bot: commands.Bot, prefix: str):
    guild: discord.Guild = bot.guilds[0]
    channel: discord.TextChannel = guild.text_channels[0]
    member: discord.Member = guild.members[0]

    # roles = await create_random_roles(guild)
    await create_random_roles(guild)
    await dpytest.set_permission_overrides(guild.me, channel, manage_roles=True)
    await channel.set_permissions(member, administrator=True)

    message: discord.Message = await channel.send(f"{prefix} manageaddrole")
    # dpytest.verify_embed(embed1, allow_text=True)

    await dpytest.run_all_events()
    await message.add_reaction("1️⃣")
    assert message.reactions == [], "The message's reactions aren't deleted"
    # assert len(member.roles) == 2
