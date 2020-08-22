import discord
from discord.ext import commands

import asyncio
from datetime import datetime
import re
import sys

from cogs.utils.deleteMessage import deleteMessage
from cogs.utils.prettyList import prettyList


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["credit", "credits", "invite"])
    async def about(self, ctx):
        """gives various informations about the bot"""
        inviteLink = f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=3537984"

        e = discord.Embed(
            title="Click here to invite me on your server!",
            description=f"SenPy is written in Python with discord.py\n{sys.version}\n{sys.platform}",
            url=inviteLink
        )

        realUsersCount = len(
            set(m for g in self.bot.guilds for m in g.members if not m.bot))

        e.add_field(name=f"Running on {len(self.bot.guilds)} servers",
                    value="Share this bot to increase this number!")
        e.add_field(name=f"Serving {sum(g.member_count for g in self.bot.guilds)} users",
                    value=f"Technically it's {realUsersCount} if you don't count bots and duplicated users but who cares")
        e.add_field(name="Github repository",
                    value="https://github.com/kugiyasan/SenPy")
        e.add_field(name="Bot ID", value=self.bot.user.id)
        e.add_field(name="You have some feedback?",
                    value="Use xd report", inline=False)
        await ctx.send(embed=e)

    @commands.command()
    async def hug(self, ctx: commands.Context):
        """Anyone wants a hug?"""
        await ctx.send("https://tenor.com/view/anime-friends-friendship-funny-best-gif-15959237")

    @commands.command(hidden=True)
    async def newhelp(self, ctx: commands.Context, category=None):
        await ctx.send("New help command coming soon!")

    @commands.command()
    async def ping(self, ctx):
        """haha ping pong"""
        await ctx.send(f"Pong! The latency is about {int(self.bot.latency*1000)} ms")

    @commands.command(hidden=True)
    async def pong(self, ctx):
        """haha ping pong"""
        await ctx.send(f"Ping... You ugly btw")

    @commands.command()
    async def say(self, ctx: commands.Context, *, words="_ _"):
        """Make this little innocent bot speak for you, you pervert"""
        attachment = await ctx.message.attachments[0].to_file() if ctx.message.attachments else None
        await deleteMessage(ctx)
        await ctx.send(words, file=attachment)

    @commands.command(aliases=["suggest", "comment", "feedback"])
    async def report(self, ctx, *, text=""):
        """Send your thoughts about this bot to the bot dev"""

        if text == "":
            await ctx.send("Write your feedback directly with the command e.g. xd feedback blah blah blah")
            return

        owner = (await self.bot.application_info()).owner
        await owner.send(f"***{ctx.author}*** has some feedback!\n{text}")
        await ctx.send("Your feedback was sent successfully!")

    @commands.is_owner()
    @commands.command(hidden=True)
    async def servers(self, ctx):
        title = f"Running on {len(self.bot.guilds)} servers"
        guilds = [
            f"{g.name} member_count: {g.member_count}" for g in self.bot.guilds]

        await prettyList(ctx, title, guilds, maxLength=0)

    @commands.command(hidden=True)
    async def thonk(self, ctx):
        """thonk emoji"""
        await deleteMessage(ctx)
        await ctx.send("<:thinking1:710563810582200350><:thinking2:710563810804498452>\n<:thinking3:710563823819554816><:thinking4:710563824079732756>")


def setup(bot):
    bot.add_cog(Info(bot))
