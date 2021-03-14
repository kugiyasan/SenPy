import discord
from discord.ext import commands
import discord.ext.test as dpytest
import pytest


@pytest.mark.asyncio
async def test_eval(bot: commands.Bot, prefix: str):
    with pytest.raises(commands.NotOwner):
        await dpytest.message(f"{prefix} eval ctx.guild.id")
