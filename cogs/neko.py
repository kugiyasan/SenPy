import discord
from discord.ext import commands

import nekos

from cogs.utils.sendEmbed import sendEmbed
from cogs.utils.deleteMessage import deleteMessage

class Neko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def neko(self, ctx: commands.Context, style='neko'):
        '''Send some cute nekos on your server!'''
        await deleteMessage(ctx)

        if not ctx.channel.is_nsfw():
            await ctx.send('Please try again in a nsfw channel')
            return

        try:
            await sendEmbed(ctx, nekos.img(style))
        except nekos.InvalidArgument as err:
            await ctx.send(err)

    @commands.command()
    async def owo(self, ctx: commands.Context, *, text:str='give me a text to owoify!'):
        '''yay cute wwitinyg >w<'''
        await deleteMessage(ctx)
        await ctx.send(nekos.owoify(text))

    @commands.command()
    async def fact(self, ctx: commands.Context):
        '''Get yo facts right!'''
        await deleteMessage(ctx)
        await ctx.send(nekos.fact())
        

def setup(bot):
    bot.add_cog(Neko(bot))
