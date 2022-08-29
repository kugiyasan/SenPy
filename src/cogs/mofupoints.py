from discord.ext import commands

import random

from .utils.dbms import db
from .utils.prettyList import prettyList


def giveMofuPoints(user, points):
    db.set_data(
        """INSERT INTO users (id, mofupoints)
            VALUES(%s, %s)
            ON CONFLICT(id)
            DO UPDATE SET mofupoints = users.mofupoints + %s""",
        (user.id, points, points),
    )


def incrementEmbedCounter(user):
    db.set_data(
        """INSERT INTO users (id, numberOfEmbedRequests)
            VALUES(%s, 1)
            ON CONFLICT(id)
            DO UPDATE SET
            numberOfEmbedRequests = users.numberOfEmbedRequests + 1""",
        (user.id,),
    )


class MofuPoints(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def getUsersLeaderboard(self, ctx, category):
        if category == "mofupoints":
            rows = db.get_data(
                """SELECT id, mofupoints FROM users
                    ORDER BY mofupoints DESC"""
            )
        elif category == "numberOfEmbedRequests":
            rows = db.get_data(
                """SELECT id, numberOfEmbedRequests FROM users
                    ORDER BY numberOfEmbedRequests DESC"""
            )
        else:
            raise ValueError(
                "Unknown category. Available args: mofupoints, numberOfEmbedRequests"
            )

        users = []

        if ctx.guild is None:
            for k, v in rows:
                user = self.bot.get_user(k)
                name = user.name if user is not None else k
                users.append((v, name))
        else:
            for k, v in rows:
                user = self.bot.get_user(k)
                if user in ctx.guild.members:
                    name = user.name if user is not None else k
                    users.append((v, name))

        return users

    @commands.command(aliases=["top"])
    async def leaderboard(self, ctx):
        """Show the leaderboard for the top fluffer"""
        users = self.getUsersLeaderboard(ctx, "mofupoints")

        title = "***MOFUPOINTS LEADERBOARD***"
        await prettyList(ctx, title, users, "points")

    @commands.command(aliases=["requesttop"])
    async def nolife(self, ctx):
        """leaderboard shows the people who requested the most pictures"""
        users = self.getUsersLeaderboard(ctx, "numberOfEmbedRequests")

        title = "***NO LIFE LEADERBOARD (people who requested the most images)***"
        await prettyList(ctx, title, users, "requests")

    @commands.cooldown(1, 3600 * 24, commands.BucketType.user)
    @commands.command()
    async def daily(self, ctx):
        """Get your daily portion of mofupoints"""
        amount = random.randint(10, 50)
        giveMofuPoints(ctx.author, amount)
        msg = f"You received {amount} points! They've been added to your balance!"
        await ctx.send(msg)


async def setup(bot: commands.Bot):
    await bot.add_cog(MofuPoints(bot))
