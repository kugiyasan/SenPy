import discord
from discord.ext import commands

import requests
from lxml import html

class Basics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def insult(self, ctx, *, member: discord.Member = None):
        """random compliment directly from the web"""
        webpage = requests.get('http://www.robietherobot.com/insult-generator.htm')
        if(webpage.status_code == 200):
            tree = html.fromstring(webpage.content)
            insultText = tree.xpath('//h1')
            if not member:
                await ctx.send("You're a " + insultText[1].text.strip())
            else:
                await ctx.send(str(member) + " is a " + insultText[1].text.strip())
        else:
            print('Error not the good status code 200 !=', webpage.status_code)

    @commands.command()
    async def stalk(self, ctx):
        """get status of all online members"""
        members = ctx.guild.members
        output = []
        for member in members:
            if member.bot:
                continue
            if not member.activities:
                if member.status != discord.Status.offline:
                    output.append(f'{member.name} is {member.status}')
                continue
            verb = str(member.activities[0].type)
            verb = verb[verb.index('.')+1:]
            if verb == 'custom':
                verb = 'saying'
            output.append(f'{member.name} is {verb} {member.activities[0].name}')
        await ctx.send('\n'.join(output))

def setup(bot):
    bot.add_cog(Basics(bot))