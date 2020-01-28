import discord
from discord.ext import commands
import urllib

description = '''my joachim Bot in Python'''
bot = commands.Bot(command_prefix='?', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def hello(ctx):
    """Says world"""
    await ctx.send("world")

@bot.command()
async def racism(ctx):
    """lololol"""
    await ctx.send("you fat nigger cunt")

@bot.command()
async def insult(ctx):
    """random compliment directly from the web"""
    webpage = urllib.request.urlopen('http://www.robietherobot.com/insult-generator.htm')
    for i, line in enumerate(webpage.readlines()):
        print(i, lines)
    
    await ctx.send("you fat nigger cunt")

@bot.command()
async def add(ctx, left : int, right : int):
    """Adds two numbers together."""
    await ctx.send(left + right)

bot.run('NjcxNzIyMzM4ODQ4MzQyMDM2.XjBkOQ.fHAIblYWIalmYUv4zNxlWnoU8K8')