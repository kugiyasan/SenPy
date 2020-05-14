import discord
from discord.ext import commands

import asyncio
import re
from cogs.utils.deleteMessage import deleteMessage

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def emoji(self, ctx: commands.Context):
        '''List all available emojis on this server + some random from other server'''
        emojisList = await ctx.guild.fetch_emojis()
        await ctx.send(' '.join(str(e) for e in emojisList))
        await ctx.send('<:choku:645454770378899457>')
        await ctx.send('<:gwumpysenko:669743618113667091>')
        print(emojisList[0])
        # https://cdn.discordapp.com/emojis/669743618113667091.png

    @commands.command()
    async def ping(self, ctx):
        '''SenPy has lower ping than Dash!!!'''
        await ctx.send(f'Pong! The latency is about {int(self.bot.latency*1000)} ms')

    @commands.command()
    async def say(self, ctx, *, words):
        '''Make this little innocent bot speak for you, you pervert'''
        await deleteMessage(ctx)

        if re.search('s[e3]nk[o0]g[o0][o0]d', words.lower().replace(' ', '')):
            await ctx.send('senko bad')
            return

        await ctx.send(words)

def setup(bot):
    bot.add_cog(Info(bot))