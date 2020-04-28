import discord
from discord.ext import commands

import nekos
import requests
from lxml import html

from cogs.utils.sendEmbed import sendEmbed
from cogs.utils.deleteMessage import deleteMessage

class Cancer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def insult(self, ctx, *, member: discord.Member = None):
        """random compliment directly from the web"""
        url = 'http://www.robietherobot.com/insult-generator.htm'
        webpage = requests.get(url)
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
    async def neko(self, ctx: commands.Context, style='neko'):
        '''Send some cute nekos on your server!'''
        await deleteMessage(ctx)

        if not ctx.channel.is_nsfw() and ctx.guild.name == 'Banana Squad':
            await ctx.send('Please try again in a nsfw channel')
            return
        style = style.lower()
        possibilities = ['feet', 'yuri', 'trap', 'futanari', 'hololewd',
                        'lewdkemo', 'solog', 'feetg', 'cum', 'erokemo', 'les',
                        'wallpaper', 'lewdk', 'ngif', 'tickle', 'lewd', 'feed',
                        'gecg', 'eroyuri', 'eron', 'cum_jpg', 'bj',
                        'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar',
                        'gasm', 'poke', 'anal', 'slap', 'hentai', 'avatar',
                        'erofeet', 'holo', 'keta', 'blowjob', 'pussy', 'tits',
                        'holoero', 'lizard', 'pussy_jpg', 'pwankg', 'classic',
                        'kuni', 'waifu', 'pat', '8ball', 'kiss', 'femdom',
                        'neko', 'spank', 'cuddle', 'erok', 'fox_girl', 'boobs',
                        'random_hentai_gif', 'smallboobs', 'hug', 'ero',
                        'smug', 'goose', 'baka', 'woof']

        if not style or style not in possibilities:
            await ctx.send(f'''Available arguments:\n```{" ".join(possibilities)}```''')
            return

        await sendEmbed(ctx, nekos.img(style))


def setup(bot):
    bot.add_cog(Cancer(bot))
