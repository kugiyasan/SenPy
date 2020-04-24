import discord
from discord.ext import commands

import inspect
import nekos
import requests
from lxml import html

class Cancer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def insult(self, ctx, *, member: discord.Member = None):
        """random compliment directly from the web"""
        webpage = requests.get('http://www.robietherobot.com/insult-generator.htm')
        if(webpage.status_code == 200):
            tree = html.fromstring(webpage.content)
            insultText = tree.xpath('//h1')[1].text.strip()
            if not member:
                await ctx.send("You're a " + insultText)
            else:
                await ctx.send(str(member) + " is a " + insultText)
        else:
            print('Error not the good status code 200 !=', webpage.status_code)

    @commands.command()
    @commands.is_nsfw()
    async def neko(self, ctx, style='neko'):
        '''Type XD neko help to see all category'''
        # .format(self.bot.command_prefix[0])
        style = style.lower()
        possibilities = ['feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo', 'solog', 'feetg', 'cum', 'erokemo', 'les',
            'wallpaper', 'lewdk', 'ngif', 'tickle', 'lewd', 'feed', 'gecg', 'eroyuri', 'eron', 'cum_jpg', 'bj', 'nsfw_neko_gif',
            'solo', 'kemonomimi', 'nsfw_avatar', 'gasm', 'poke', 'anal', 'slap', 'hentai', 'avatar', 'erofeet', 'holo', 'keta',
            'blowjob', 'pussy', 'tits', 'holoero', 'lizard', 'pussy_jpg', 'pwankg', 'classic', 'kuni', 'waifu', 'pat', '8ball',
            'kiss', 'femdom', 'neko', 'spank', 'cuddle', 'erok', 'fox_girl', 'boobs', 'random_hentai_gif', 'smallboobs', 'hug',
            'ero', 'smug', 'goose', 'baka', 'woof']
        if style == 'help':
            await ctx.send(f'Available arguments:\n```{" ".join(possibilities)}```')
            return
        if not style or style not in possibilities:
            await ctx.send(f'Choose an valid argument! Available arguments:\n```{" ".join(possibilities)}```')
            return
        e = discord.Embed(
            type='image',
            color=discord.Colour.gold())
        e.set_image(url=nekos.img(style))
        await ctx.send(embed=e)
        

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
    bot.add_cog(Cancer(bot))