# https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html
# https://github.com/nobodyme/reddit-fetch.git
# https://github.com/runarsf/rufus
# https://praw.readthedocs.io/en/latest/getting_started/quick_start.html

import discord
from discord.ext import commands

try:
    from myToken import token
except:
    from yourToken import token

description = '''JOACHIM IS THE MASTER OF THE UNIVERSE'''
occupation = discord.Activity(type=discord.ActivityType.playing, name='with Fox Goddess')
bot = commands.Bot(command_prefix='XD ', description=description, activity=occupation)

extensions = ['botCommands.basics',
            'botCommands.dev',
            'botCommands.reddit',
            'botCommands.welcome']

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} running on {len(bot.guilds)} servers - id: {bot.user.id}')
    for g in bot.guilds:
        print(g.name + ' member_count: ' + str(g.member_count))
    print()

@bot.command()
@commands.is_owner()
async def reloadExt(ctx):
    """reload the extensions"""
    for ext in extensions:
        bot.reload_extension(ext)
    print('Reloading successfully finished!')

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