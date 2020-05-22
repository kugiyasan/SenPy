import discord
from discord.ext import commands

import asyncio
import re
import sys
from cogs.utils.deleteMessage import deleteMessage

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def about(self, ctx):
        await ctx.send('SenPy is running on:\n' + sys.version + '\n' + sys.platform)

    @commands.command(aliases=['thonk', 'thinking'])
    async def chika(self, ctx, expression=None):
        await deleteMessage(ctx)
        # guild = await self.bot.fetch_guild(700719623917666336)
        # emojisList = await guild.fetch_emojis()
        # await ctx.send(''.join(str(e) for e in emojisList))

        await ctx.send('<:thinking1:710563810582200350><:thinking2:710563810804498452>\n<:thinking3:710563823819554816><:thinking4:710563824079732756>')

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
    async def say(self, ctx: commands.Context, *, words=''):
        '''Make this little innocent bot speak for you, you pervert'''

        if re.search('s[e3]nk[o0]g[o0][o0]d', words.lower().replace(' ', '')):
            await deleteMessage(ctx)
            await ctx.send('senko bad')
            return

        if ctx.message.attachments:
            PATH = f'media/say_{ctx.author.name}.png'
            await ctx.message.attachments[0].save(PATH)
            await deleteMessage(ctx)
            await ctx.send(words, file=discord.File(PATH))
            return

        await deleteMessage(ctx)
        await ctx.send(words)

def setup(bot):
    bot.add_cog(Info(bot))