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

extensions = ['botCommands.basics',
            'botCommands.dev',
            'botCommands.welcome',]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} running on {len(bot.guilds)} servers - id: {bot.user.id}')
    for g in bot.guilds:
        print(g.name + ' member_count: ' + str(g.member_count))
    print()



ua = UserAgent(fallback='Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11')
@bot.command(name='mofumofu')
async def sendPic(ctx):
    """Send blessing to the server!"""
    while len(URLdata) < 100:
        getPics()
        
    print('requesting an image to reddit')
    image = requests.get(URLdata.pop(), allow_redirects=False)
    if(image.status_code == 200):
        try:
            discordImage = discord.File(io.BytesIO(image.content), filename='praiseTheLord.png')
            await ctx.send(file=discordImage)
            return
        except:
            print('Error image not sent')
    else:
        print('Error not the good status code 200 !=', image.status_code)

after = 'null'
URLdata = []
def getPics():
    global after
    url = 'https://www.reddit.com/r/ChurchOfSenko/new/.json?after=' + after
    print('requesting json file to reddit')
    response = requests.get(url, headers={'User-agent': ua.random})

    if not response.ok:
        print("Error check the name of the subreddit", response.status_code)
        return

    data = response.json()['data']['children']
    after = response.json()['data']['after']
    random.shuffle(data)
    for child in data:
        image_url = child['data']['url']
        if 'imgur' in image_url:
            image_url += '.jpeg'
        if '.png' in image_url or '.jpg' in image_url or '.jpeg' in image_url:
            URLdata.append(image_url)
    print(f'{len(URLdata)} urls added to the list')

@bot.command()
@commands.is_owner()
async def reloadExt(ctx):
    """reload the commands to make it faster and easier to apply changes"""
    for ext in extensions:
        bot.reload_extension(ext)

@bot.command()
@commands.is_owner()
async def stop(ctx):
    """DON'T"""
    print('\nlogging out...')
    await bot.logout()

if __name__ == "__main__":
    for ext in extensions:
        bot.load_extension(ext)

    bot.run(token)