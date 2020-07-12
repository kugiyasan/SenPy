import discord
from discord.ext import commands

import asyncio
import random


class RussianRoulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["rr"])
    async def russianroulette(self, ctx, *adversaries: discord.Member):
        """Remake of KiryaBRO#3091's russian roulette command"""
        """Haha guns goes pew pew"""
        await ctx.send("https://tenor.com/view/gun-pistol-revolver-gif-9832859")
        await ctx.send(f"Russian Roulette game!! Take the gun, spin the barrel, shoot and hope to survive!")

        players = list(adversaries)
        if len(players) == 0:
            players.append(self.bot.user)

        players.insert(0, ctx.author)
        NUMBER_OF_PLAYERS = len(players)
        turn = 0

        def checkresponse(m):
            return (m.channel == ctx.channel
                    and m.author == players[turn])

        # MAIN LOOP
        while True:
            await ctx.send(f"{players[turn].mention}, type s (shoot) or q (quit)")
            if players[turn] != self.bot.user:
                try:
                    m = await self.bot.wait_for(
                        "message",
                        timeout=30.0,
                        check=checkresponse
                    )
                except asyncio.TimeoutError:
                    await ctx.send(f"Stopping russian roulette, timeout expired\n{players[turn].mention} loses!")
                    return

                if m.content.lower() in ("stop", "exit", "quit", "q"):
                    await ctx.send("Stopping russian roulette")
                    return

                if m.content.lower() not in ("pow", "s", "shoot"):
                    continue

            await ctx.send("https://tenor.com/view/cameron-monaghan-gif-5508114")
            await asyncio.sleep(1)

            if random.randint(0, 5):
                await ctx.send(f"{players[turn].mention}, click... you are lucky, my friend...")
                turn = (turn + 1) % NUMBER_OF_PLAYERS
            else:
                await ctx.send(f"***POW!!!!*** {players[turn].mention} got shot and died.")
                return


def setup(bot):
    bot.add_cog(RussianRoulette(bot))
