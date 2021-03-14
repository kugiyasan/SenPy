import discord
from discord.ext import commands

import os
import dotenv

from cogs.utils.get_extensions import get_extensions
from cogs.utils.get_prefixes import get_prefixes


def create_bot() -> commands.Bot:
    dotenv.load_dotenv()
    prefix = os.environ["DEFAULT_COMMAND_PREFIX"]
    intents = discord.Intents.default()
    intents.members = True

    bot = commands.Bot(
        command_prefix=get_prefixes,
        activity=discord.Game(name=f"{prefix} help | {prefix} about"),
        intents=intents,
    )

    for ext in get_extensions():
        bot.load_extension(ext)

    return bot


if __name__ == "__main__":
    bot = create_bot()
    bot.run(os.environ["DISCORD_TOKEN"])
