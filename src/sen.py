import discord
from discord.ext import commands

import asyncio
import os
import dotenv

from cogs.utils.get_extensions import get_extensions
from cogs.utils.get_prefixes import get_prefixes


async def create_bot() -> commands.Bot:
    dotenv.load_dotenv()
    prefix = os.environ["DEFAULT_COMMAND_PREFIX"]
    intents = discord.Intents.default()
    intents.members = True

    bot = commands.Bot(
        command_prefix=get_prefixes,
        activity=discord.Game(name=f"{prefix} help | {prefix} about"),
        intents=intents,
    )

    return bot


async def main() -> None:
    print("create bot")
    bot = await create_bot()

    # start the client
    async with bot:
        for ext in get_extensions():
            print(f"loading {ext}")
            await bot.load_extension(ext)

        print("bot start")
        await bot.start(os.environ["DISCORD_TOKEN"])
        # bot.run(os.environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
