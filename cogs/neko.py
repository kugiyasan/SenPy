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


def setup(bot):
    bot.add_cog(Neko(bot))
