import discord
from discord.ext import commands

from functools import lru_cache
import os

from cogs.utils.dbms import conn, cursor

PREFIX = os.environ["DEFAULT_COMMAND_PREFIX"]


@lru_cache
def get_guild_prefix(guildID: int):
    try:
        with conn:
            query = "SELECT command_prefix FROM guilds WHERE id = %s"
            cursor.execute(query, (guildID,))
            return cursor.fetchone()[0]
    except TypeError:
        return None


def get_prefixes(bot: commands.Bot, message: discord.Message):
    prefix = PREFIX
    if message.guild is not None:
        prefix = get_guild_prefix(message.guild.id) or prefix

    return commands.when_mentioned_or(prefix + " ", prefix)(bot, message)
