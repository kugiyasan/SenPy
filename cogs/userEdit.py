import discord
from discord.ext import commands

import io

from cogs.utils.deleteMessage import deleteMessage

class UserEdit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def renameBot(self, ctx, name):
        await self.bot.user.edit(username=name)

    @commands.command()
    async def activity(self, ctx, *, string):
        occupation = discord.Activity(type=discord.ActivityType.playing, name=string)
        await self.bot.change_presence(activity=occupation)

    @commands.command()
    async def changeAvatar(self, ctx):
        if not ctx.message.attachments:
            await ctx.send('No image attached with your message!')

        image = await ctx.message.attachments[0].read()
        await self.bot.user.edit(avatar=io.BytesIO(image).getvalue())

    @commands.command()
    async def hypesquad(self, ctx, house):
        house = house.lower()

        if house == 'bravery':
            house = discord.HypeSquadHouse.bravery
        elif house == 'brilliance':
            house = discord.HypeSquadHouse.brilliance
        elif house == 'balance':
            house = discord.HypeSquadHouse.balance
        elif house == 'none':
            house = None
        else:
            await ctx.send('Unknown hypesquad house')
            return

        await self.bot.user.edit(house=house)

def setup(bot):
    bot.add_cog(UserEdit(bot))