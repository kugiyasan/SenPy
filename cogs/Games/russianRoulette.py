import discord
from discord.ext import commands

import asyncio
import random

class RussianRoulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['rr'])
    async def russianroulette(self, ctx):
        """Remake of KiryaBRO#3091's russian roulette command"""
        """Haha guns goes pew pew"""
        await ctx.send(f'{ctx.author.mention}, would you like to play "russian roulette" game?')
        
        def checkresponse(m):
            return m.channel == ctx.channel
        
        # MAIN LOOP
        while True:
            await ctx.send("Type s (shoot) or q (quit)")
            try:
                m = await self.bot.wait_for(
                    'message',
                    timeout=60.0,
                    check=checkresponse
                )
            except asyncio.TimeoutError:
                await ctx.send('Stopping russian roulette, timeout expired')
                return

            if m.content.lower() in ('stop', 'exit', 'quit', 'q'):
                await ctx.send('Stopping russian roulette')
                return

            if m.content.lower() not in ('pow', 's', 'shoot'):
                continue

            thrillSentences = (
                "are you lucky enough?...",
                "well...",
                "don't hesitate...",
                "tick tock tick tock..."
            )
            
            await ctx.send(f"Secret: {m.author.mention}, " + random.choice(thrillSentences))
            asyncio.sleep(1)

            if random.randint(0, 5):
                await ctx.send(f"{m.author.mention}, you are safe... for now...")
            else:
                await ctx.send(f"{m.author.mention} got shot.")
                return

def setup(bot):
    bot.add_cog(RussianRoulette(bot))