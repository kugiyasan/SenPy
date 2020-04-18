# https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html
# https://github.com/nobodyme/reddit-fetch.git
# https://github.com/runarsf/rufus
# https://praw.readthedocs.io/en/latest/getting_started/quick_start.html
import discord
from discord.ext import commands
import requests
import random
from fake_useragent import UserAgent
import io
try:
    from myToken import token
except:
    from yourToken import token

# 'https://www.reddit.com/r/ChurchOfSenko/'
# https://www.reddit.com/r/ChurchOfSenko/top/.json?sort=top&t=all&limit=10
# 'https://anime.icotaku.com/uploads/personnages/personnage_27974/perso_anime_HjxQjd8HmNAQ8Hc.png'

description = '''JOACHIM IS THE MASTER OF THE UNIVERSE'''
occupation = discord.Activity(type=discord.ActivityType.playing, name='with Fox Goddess')
# bot = commands.Bot(command_prefix='8==D ', description=description, activity=occupation)
bot = commands.Bot(command_prefix='XD ', description=description, activity=occupation)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} running on {len(bot.guilds)} servers - id: {bot.user.id}')
    for g in bot.guilds:
        print(g.name + ' member_count: ' + str(g.member_count))

@bot.command()
async def insult(ctx):
    """random compliment directly from the web"""
    webpage = requests.get('http://www.robietherobot.com/insult-generator.htm')#.readlines()[115].decode('utf-8')
    if(webpage.status_code == 200):
        print(webpage.text)
        await ctx.send("You're a " + webpage.text[115][12:webpage.index('<')])
    else:
        print('Error not the good status code 200 !=', webpage.status_code)
    
# class Slapper(commands.Converter):
#     async def convert(self, ctx, argument):
#         to_slap = random.choice(ctx.guild.members)
#         return '{0.author} slapped {1} because *{2}*'.format(ctx, to_slap, argument)

# @bot.command()
# async def slap(ctx, *, reason: Slapper):
#     """SLAP LIKE NOW"""
#     await ctx.send(reason)

@bot.command()
async def joined(ctx, *, member: discord.Member = None):
    """tells the time that a member joined this server"""
    if not member:
        member = ctx.author
    await ctx.send('{0} joined on {0.joined_at}'.format(member))

@bot.command()
async def stalk(ctx):
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

ua = UserAgent(fallback='Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11')
@bot.command(name='mofumofu')
async def sendPic(ctx, limit : int = 50):
    """Send blessing to the server!"""
    url = 'https://www.reddit.com/r/ChurchOfSenko/new/.json?limit=' + str(limit)
    response = requests.get(url, headers={'User-agent': ua.random})

    if not response.ok:
        print("Error check the name of the subreddit", response.status_code)
        return

    data = response.json()['data']['children']
    print('number of post received', len(data))
    for i in range(len(data)):
        image_url = random.choice(data)['data']['url']
        if 'imgur' in image_url:
            image_url += '.jpeg'
        elif not('.png' in image_url or '.jpg' in image_url or '.jpeg' in image_url):
            continue
            
        image = requests.get(image_url, allow_redirects=False)
        if(image.status_code == 200):
            try:
                discordImage = discord.File(io.BytesIO(image.content), filename='praiseTheLord.png')
                await ctx.send(file=discordImage)
                return
            except:
                print('Error image not sent')
        else:
            print('Error not the good status code 200 !=', image.status_code)


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member

@bot.command()
@commands.is_owner()
async def reloadCog(ctx):
    """reload the commands to make it faster and easier to apply changes"""
    bot.remove_cog('Greetings')
    bot.add_cog(Greetings(bot))

bot.add_cog(Greetings(bot))

@bot.command()
@commands.is_owner()
async def stop(ctx):
    """you can't use this"""
    print('\nlogging out...')
    await bot.logout()


bot.run(token)