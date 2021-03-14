from discord.ext import commands
import discord.ext.test as dpytest
import pytest


# TODO about, say, sAy, poll

@pytest.mark.asyncio
async def test_ping(bot: commands.Bot, prefix: str):
    await dpytest.message(f"{prefix} ping")
    dpytest.verify_message("Pong! The latency is about", contains=True)


@pytest.mark.asyncio
async def test_pong(bot: commands.Bot, prefix: str):
    await dpytest.message(f"{prefix} pong")
    dpytest.verify_message("Ping... You ugly btw")
