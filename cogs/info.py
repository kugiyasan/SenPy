import discord
from discord.ext import commands

import asyncio
from cogs.utils.deleteMessage import deleteMessage

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def count(self, ctx: commands.Context):
        n = 1

        def checkresponse(m):
            return (m.author == ctx.author
                and m.channel == ctx.channel)

        while 1:
            await ctx.send(n)
            try:
                msg = await self.bot.wait_for('message', timeout=10.0, check=checkresponse)
            except asyncio.TimeoutError:
                await ctx.send('Why you stopped counting? Is it because you can\'t count further?')
                break

            if msg.content != str(n+1):
                await ctx.send('That\'s not the answer I was expecting b-b-baka!!!')
                break
            n += 2

    @commands.command()
    async def emoji(self, ctx: commands.Context):
        emojisList = await ctx.guild.fetch_emojis()
        await ctx.send(' '.join(str(e) for e in emojisList))
        await ctx.send('<:choku:645454770378899457>')
        await ctx.send('<:gwumpysenko:669743618113667091>')
        print(emojisList[0])
        # https://cdn.discordapp.com/emojis/669743618113667091.png

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! The latency is about {int(self.bot.latency*1000)} ms')

    @commands.command()
    async def say(self, ctx, *, words):
        await deleteMessage(ctx)
        await ctx.send(words)

def setup(bot):
    bot.add_cog(Info(bot))