import discord
from discord.ext import commands

import asyncio
import re
import sys

from cogs.utils.deleteMessage import deleteMessage
from cogs.utils.prettyList import prettyList


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['credit', 'credits', 'invite'])
    async def about(self, ctx):
        """gives various informations about the bot"""
        inviteLink = f'https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=3537984'

        e = discord.Embed(
            title='Click here to invite me on your server!',
            description=f'SenPy is written in Python with discord.py\n{sys.version}\n{sys.platform}',
            url=inviteLink
        )

        e.add_field(name=f'Running on {len(self.bot.guilds)} servers', value='Share this bot to increase this number!')
        e.add_field(name='Github repository', value='https://github.com/kugiyasan/SenPy')
        e.add_field(name='Bot ID', value=self.bot.user.id)
        e.add_field(name='You have some feedback?', value='Use xd report', inline=False)
        await ctx.send(embed=e)

    @commands.command()
    async def thonk(self, ctx):
        """thonk emoji"""
        await deleteMessage(ctx)
        await ctx.send('<:thinking1:710563810582200350><:thinking2:710563810804498452>\n<:thinking3:710563823819554816><:thinking4:710563824079732756>')

    @commands.command()
    async def hug(self, ctx: commands.Context):
        """Anyone wants a hug?"""
        await ctx.send('https://tenor.com/view/anime-friends-friendship-funny-best-gif-15959237')

    @commands.command(hidden=True)
    async def newhelp(self, ctx: commands.Context, category=None):
        await ctx.send('New help command coming soon!')

    @commands.command()
    async def ping(self, ctx):
        """haha ping pong"""
        await ctx.send(f'Pong! The latency is about {int(self.bot.latency*1000)} ms')

    @commands.command()
    async def say(self, ctx: commands.Context, *, words=''):
        """Make this little innocent bot speak for you, you pervert"""
        if words == '':
            await ctx.send("You need to add text or image in your message!")
            return

        # TODO don't save the file locally, send it directly
        attachment = None

        if ctx.message.attachments:
            PATH = f'media/say_{ctx.author.name}.png'
            await ctx.message.attachments[0].save(PATH)
            attachment = discord.File(PATH)

        await deleteMessage(ctx)
        await ctx.send(words, file=attachment)

    @commands.is_owner()
    @commands.command(hidden=True)
    async def servers(self, ctx):
        title = f"Running on {len(self.bot.guilds)} servers"
        guilds = [f'{g.name} member_count: {g.member_count}' for g in self.bot.guilds]

        await prettyList(ctx, title, guilds, maxLength=0)

    @commands.command(aliases=['suggest', 'comment', 'feedback'])
    async def report(self, ctx, *, text=''):
        """Send your thoughts about this bot to the bot dev"""

        if text == '':
            await ctx.send('Write your feedback directly with the command e.g. xd feedback blah blah blah')
            return

        channel = await self.bot.get_user(self.bot.owner_id).create_dm()
        await channel.send(f"***{ctx.author}*** has some feedback!\n{text}")
        await ctx.send("Your feedback was sent successfully!")

def setup(bot):
    bot.add_cog(Info(bot))