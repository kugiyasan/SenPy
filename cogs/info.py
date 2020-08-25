import discord
from discord.ext import commands

from datetime import datetime
import sys

from cogs.utils.deleteMessage import deleteMessage


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.startTime = datetime.now()

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

        uptime = datetime.now() - self.startTime

        contributors = (502588820051591190, 534267874794143745,
                        256149662979850251, 230702257480400896)
        contributors = "\n".join(str(self.bot.get_user(userid))
                                 for userid in contributors)

        e.add_field(name=f"Running on {len(self.bot.guilds)} servers",
                    value="Share this bot to increase this number!")
        e.add_field(name=f"Serving {sum(g.member_count for g in self.bot.guilds)} users",
                    value=f"Technically it's {realUsersCount} if you don't count bots and duplicated users but who cares")
        e.add_field(name="Github repository",
                    value="https://github.com/kugiyasan/SenPy")
        e.add_field(name="Owner", value=(await self.bot.application_info()).owner)
        e.add_field(name="Bot ID", value=self.bot.user.id)
        e.add_field(name="Uptime", value=str(uptime)[:-7])
        e.add_field(name="Latency", value=f"{int(self.bot.latency*1000)} ms")
        e.add_field(name="Contributors", value=contributors)
        e.add_field(name="Support server", value="https://discord.gg/axTWGsc")
        e.add_field(name="You have some feedback?", value="Use xd report")
        await ctx.send(embed=e)

    @commands.command()
    async def hug(self, ctx: commands.Context):
        """Anyone wants a hug?"""
        await ctx.send("https://tenor.com/view/anime-friends-friendship-funny-best-gif-15959237")

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

    @commands.command(aliases=["SaY"])
    async def sAy(self, ctx: commands.Context, *, words="_ _"):
        """MaKe tHiS LiTtLe iNnOcEnT BoT SpEaK FoR YoU, yOu pErVeRt"""
        alternateCase = ""
        for i, c in enumerate(words.lower()):
            if i % 2 == 0:
                alternateCase += c
            else:
                alternateCase += c.upper()

        await self.say(ctx, words=alternateCase)

    @commands.command(aliases=["suggest", "comment", "feedback"])
    async def report(self, ctx, *, text=""):
        """Send your thoughts about this bot to the bot dev"""

        if text == "":
            await ctx.send("Write your feedback directly with the command e.g. xd feedback blah blah blah")
            return

        owner = (await self.bot.application_info()).owner
        await owner.send(f"***{ctx.author}*** has some feedback!\n{text}")
        await ctx.send("Your feedback was sent successfully!")


def setup(bot: commands.Bot):
    bot.add_cog(Info(bot))
