import discord.ext.test as dpytest
import pytest


@pytest.mark.asyncio
async def test_ping(bot, prefix):
    await dpytest.message(f"{prefix} ping")
    dpytest.verify_message("Pong! The latency is about", contains=True)
