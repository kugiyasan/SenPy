import discord
from discord.ext import commands

import json
from cogs.utils.configJson import getValueJson, updateValueJson
from cogs.utils.deleteMessage import deleteMessage

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

    @commands.command(aliases=['top'])
    async def leaderboard(self, ctx):
        """Show the leaderboard for the top fluffer"""
        data = await getValueJson('users')
        users = sorted([(v['mofuPoints'], k) for k, v in data.items()], reverse=True)
        users = [user for user in users if self.bot.get_user(int(user[1])) in ctx.guild.members]

        emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
        output = []
        for i in range(min(len(emojis), len(users))):
            name = self.bot.get_user(int(users[i][1])).name
            output.append(emojis[i] + f' {name}: {users[i][0]} points')

        await ctx.send('\n'.join(output))

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