import discord
from discord.ext import commands

import json
from cogs.utils.configJson import getValueJson, updateValueJson
from cogs.utils.deleteMessage import deleteMessage
from cogs.utils.prettyList import prettyList

async def giveMofuPoints(user, points):
    path = 'users', str(user.id), 'mofuPoints'
    userPoint = await getValueJson(*path, default=0)
    await updateValueJson(userPoint+points, *path)

async def incrementEmbedCounter(user):
    path = 'users', str(user.id), 'numberOfEmbedRequested'
    userPoint = await getValueJson(*path, default=0)
    userPoint += 1
    await updateValueJson(userPoint, *path)
    
    if userPoint % 5 == 0:
        await giveMofuPoints(user, 1)

class MofuPoints(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def getUsersLeaderboard(self, ctx, category):
        data = await getValueJson('users')
        users = []

        for k, v in data.items():
            user = self.bot.get_user(int(k))
            if user in ctx.guild.members:
                try:
                    users.append((v[category], user.name))
                except:
                    pass
        
        return sorted(users, reverse=True)

    @commands.command(aliases=['top'])
    async def leaderboard(self, ctx):
        """Show the leaderboard for the top fluffer"""
        users = await self.getUsersLeaderboard(ctx, 'mofuPoints')

        title = '***MOFUPOINTS LEADERBOARD***'
        await prettyList(ctx, title, users, 'points')

    @commands.command(aliases=['imagetop'])
    async def nolife(self, ctx):
        """Show the leaderboard for who has requested the most images"""
        users = await self.getUsersLeaderboard(ctx, 'numberOfEmbedRequested')

        title = '***NO LIFE LEADERBOARD***'
        await prettyList(ctx, title, users, 'requests')

    @commands.command(hidden=True, aliases=['senkobad', 'rmt', 'marubestgirl', 'meguminbestgirl', 'hifumibestgirl'])
    async def chikabestgirl(self, ctx):
        # This is a secret command, congrats to you if you've found it!
        await deleteMessage(ctx)

        path = 'users', str(ctx.author.id), 'claimedEasterEgg'
        alreadyClaimed = await getValueJson(*path, default=False)
        if alreadyClaimed:
            return

        await updateValueJson(True, *path)
        await giveMofuPoints(ctx.author, 100)

def setup(bot):
    bot.add_cog(MofuPoints(bot))