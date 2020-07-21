import discord
from discord.ext import commands

from cogs.utils.dbms import conn, cursor
from cogs.utils.deleteMessage import deleteMessage
from cogs.utils.prettyList import prettyList


async def giveMofuPoints(user, points):
    with conn:
        cursor.execute("""INSERT INTO users (id, mofupoints)
                        VALUES(%s, %s) 
                        ON CONFLICT(id) 
                        DO UPDATE SET mofupoints = users.mofupoints + %s""", (user.id, points, points))


async def incrementEmbedCounter(user):
    with conn:
        cursor.execute("""INSERT INTO users (id, numberOfEmbedRequests)
                        VALUES(%s, 1) 
                        ON CONFLICT(id) 
                        DO UPDATE SET numberOfEmbedRequests = users.numberOfEmbedRequests + 1""", (user.id,))


class MofuPoints(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def getUsersLeaderboard(self, ctx, category):
        if category == "mofupoints":
            cursor.execute("""SELECT id, mofupoints FROM users
                                    ORDER BY mofupoints DESC""")
            rows = cursor.fetchall()
        elif category == "numberOfEmbedRequests":
            cursor.execute("""SELECT id, numberOfEmbedRequests FROM users
                                    ORDER BY numberOfEmbedRequests DESC""")
            rows = cursor.fetchall()
        else:
            raise ValueError(
                "Unknown category. Available arguments: mofupoints, numberOfEmbedRequests")

        users = []

        for k, v in rows:
            user = self.bot.get_user(k)
            if user in ctx.guild.members:
                users.append((v, user.name))

        return users

    @commands.command(aliases=['top'])
    async def leaderboard(self, ctx):
        """Show the leaderboard for the top fluffer"""
        users = await self.getUsersLeaderboard(ctx, 'mofupoints')

        title = '***MOFUPOINTS LEADERBOARD***'
        await prettyList(ctx, title, users, 'points')

    @commands.command(aliases=['imagetop'])
    async def nolife(self, ctx):
        """Show the leaderboard for who has requested the most images"""
        users = await self.getUsersLeaderboard(ctx, 'numberOfEmbedRequests')

        title = '***NO LIFE LEADERBOARD***'
        await prettyList(ctx, title, users, 'requests')

    @commands.command(hidden=True, aliases=['senkobad', 'rmt', 'marubestgirl', 'meguminbestgirl', 'hifumibestgirl'])
    async def chikabestgirl(self, ctx):
        # This is a secret command, congrats to you if you've found it!
        await deleteMessage(ctx)

        with conn:
            cursor.execute(
                "SELECT easterEggClaimed FROM users WHERE id = %s", (ctx.author.id,))
            alreadyClaimed = cursor.fetchone()
            cursor.execute("""INSERT INTO users (id, easterEggClaimed)
                            VALUES(%s, 1) 
                            ON CONFLICT(id) 
                            DO UPDATE SET easterEggClaimed = TRUE""", (ctx.author.id,))

        if alreadyClaimed[0]:
            return

        await giveMofuPoints(ctx.author, 100)


def setup(bot):
    bot.add_cog(MofuPoints(bot))
