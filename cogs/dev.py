import discord
from discord.ext import commands

import asyncio
import random

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        pass
        # print(discord.Permissions.send_messages)

    @commands.command(hidden=True)
    async def test(self, ctx: commands.Context):
        file = discord.File("media/hanamaru.jpg", filename="image.png")
        embed = discord.Embed()
        embed.set_image(url="attachment://image.png")
        await ctx.send(file=file, embed=embed)
        
    @commands.command()
    async def num(self, ctx: commands.Context):
        await ctx.send(ctx.message.author.mention + ' Would you like to play "guess number" game?')
        randomnum = random.randint(1, 100)
        attempts = 5

        def check(m):
            return (m.author == ctx.author
                and m.channel == ctx.channel)

        while attempts > 0:
            guess = ""

            while not guess.isdigit():
                await ctx.send(ctx.author.mention + ', write a natural number from 1 to 100 or q (quit)')

                try:
                    msg = await self.bot.wait_for('message', timeout=15, check=check)
                    guess = msg.content
                except asyncio.TimeoutError:
                    await ctx.send('Timeout exceed, quitting...')
                    return
                except ValueError:
                    pass
            
            quitWords = ('q', 'quit', 'exit')
            if guess in quitWords:
                await ctx.send('Quitting...')
                return
            
            guess = int(guess)

            if guess < randomnum:
                await ctx.send('It is bigger')
            elif guess > randomnum:
                await ctx.send('It is smaller')
            else:
                await ctx.send(f'Ladies and gentlemen, {ctx.author.mention} got it. My number was: {randomnum}')
                return

            attempts -= 1

        await ctx.send(f'You failed! My number was {randomnum}')


def setup(bot):
    bot.add_cog(Dev(bot))

