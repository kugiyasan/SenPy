import discord
from discord.ext import commands
from typing import Union


async def deleteMessage(obj: Union[commands.Context, discord.Message]) -> None:
    if not isinstance(obj, discord.Message):
        obj = obj.message

    try:
        await obj.delete()
    except (discord.Forbidden, discord.errors.NotFound):
        pass
