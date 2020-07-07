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

        for adversary in adversaries:
            def confirmParticipation(m):
                return (m.channel == ctx.channel
                        and m.author == adversary)

            await ctx.send(f"{adversary.mention}, do you want to play a game of Russian Roulette?")
            try:
                m = await self.bot.wait_for(
                    "message",
                    timeout=15.0,
                    check=confirmParticipation
                )
            except asyncio.TimeoutError:
                await ctx.send(f"{adversary.mention}, I'll take that as a no")
                players.remove(adversary)

            if m.content.lower() in ("y", "yes"):
                await ctx.send("Perfect, you're in the game!")
            elif m.content.lower() in ("n", "no"):
                await ctx.send("Okay, I'll exclude you from the game")
                players.remove(adversary)
            else:
                await ctx.send("Can you answer more clearly with a (y)es or a (n)o?")

        players.insert(0, ctx.author)
        NUMBER_OF_PLAYERS = len(players)
        turn = 0

        def checkresponse(m):
            return (m.channel == ctx.channel
                    and m.author == players[turn])

        # MAIN LOOP
        while True:
            await ctx.send(f"{players[turn].mention}, type s (shoot) or q (quit)")
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
