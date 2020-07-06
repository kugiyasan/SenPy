import discord
from discord.ext import commands

from cogs.utils.dbms import conn
from cogs.utils.deleteMessage import deleteMessage
from cogs.utils.prettyList import prettyList


async def giveMofuPoints(user, points):
    with conn:
        conn.execute("""INSERT INTO users (id, mofupoints)
                        VALUES(?, ?) 
                        ON CONFLICT(id) 
                        DO UPDATE SET mofupoints = mofupoints + ?""", (user.id, points, points))


async def incrementEmbedCounter(user):
    with conn:
        conn.execute("""INSERT INTO users (id, numberOfEmbedRequests)
                        VALUES(?, 1) 
                        ON CONFLICT(id) 
                        DO UPDATE SET numberOfEmbedRequests = numberOfEmbedRequests + 1""", (user.id,))


class MofuPoints(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def getUsersLeaderboard(self, ctx, category):
        if category == "mofupoints":
            rows = conn.execute("""SELECT id, mofupoints FROM users
                                    ORDER BY mofupoints DESC""").fetchall()
        elif category == "numberOfEmbedRequests":
            rows = conn.execute("""SELECT id, numberOfEmbedRequests FROM users
                                    ORDER BY numberOfEmbedRequests DESC""").fetchall()
        else:
            raise ValueError("Unknown category. Available arguments: mofupoints, numberOfEmbedRequests")

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
            alreadyClaimed = conn.execute("SELECT easterEggClaimed FROM users WHERE id = ?", (ctx.author.id,)).fetchone()
            conn.execute("""INSERT INTO users (id, easterEggClaimed)
                            VALUES(?, 1) 
                            ON CONFLICT(id) 
                            DO UPDATE SET easterEggClaimed = 1""", (ctx.author.id,))

        if alreadyClaimed[0]:
            return

        await giveMofuPoints(ctx.author, 100)


def setup(bot):
    bot.add_cog(MofuPoints(bot))
