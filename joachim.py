# https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html
# https://github.com/nobodyme/reddit-fetch.git
# https://github.com/runarsf/rufus
# https://praw.readthedocs.io/en/latest/getting_started/quick_start.html

# if you use stub e.g. f(member: discord.Member), autocomplete is going to work

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
            'botCommands.events',
            'botCommands.reddit']

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} running on {len(bot.guilds)} servers - id: {bot.user.id}')
    for g in bot.guilds:
        print(g.name + ' member_count: ' + str(g.member_count))
    print()

@bot.command(hidden=True)
@commands.is_owner()
async def reloadExt(ctx: commands.Context):
    """reload the extensions"""
    await ctx.message.delete()
    for ext in extensions:
        bot.reload_extension(ext)
    print('Reloading successfully finished!')

@bot.command(hidden=True)
@commands.is_owner()
async def stop(ctx: commands.Context):
    """DON'T"""
    await ctx.message.delete()
    print('\nlogging out...')
    await bot.logout()

if __name__ == "__main__":
    for ext in extensions:
        bot.load_extension(ext)

    bot.run(token)