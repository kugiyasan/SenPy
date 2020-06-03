# https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html
# https://github.com/nobodyme/reddit-fetch.git
# https://github.com/runarsf/rufus

#* Stubs or type hints (e.g. member: discord.Member) helps autocomplete

import discord
from discord.ext import commands

import itertools
import json
import logging
import pathlib
import sys

from cogs.utils.deleteMessage import deleteMessage
from cogs.utils.configJson import getValueJson

from discordToken import token

def variations(prefix):
    bothCase = [(c.upper(), c.lower()) for c in prefix]
    caseUnsensitive = itertools.product(*bothCase)
    output = [''.join(s) for s in caseUnsensitive]
    withSpace = [''.join(s)+' ' for s in output]
    return withSpace + output

async def prefixes(bot: commands.Bot, message: discord.Message):
    try:
        prefix = await getValueJson('guilds', message.guild.name, 'command_prefix', default='xd')
    except:
        prefix = 'xd'
        
    return variations(prefix)

description = '''JOACHIM IS THE MASTER OF THE UNIVERSE'''
occupation = discord.Activity(type=discord.ActivityType.playing,
                                name='with Fox Goddess')

bot = commands.Bot(command_prefix=prefixes,
                    description=description,
                    activity=occupation)
# bot.remove_command('help')

#! cogs.Maths.dataVisualizer and cogs.nn won't run on pypy
extensions = ('cogs.Games.mastermind',
            # 'cogs.Games.wordStory',
            # 'cogs.Maths.mathsEquations',
            'cogs.admin',
            'cogs.dev',
            'cogs.events',
            'cogs.info',
            'cogs.memes',
            'cogs.mofupoints',
            'cogs.neko',
            'cogs.reddit',
            'cogs.thisDoesNotExist',
            'cogs.voice')

pythonExclusiveExtensions = (
    'cogs.Maths.dataVisualizer',
    'cogs.nn')
loadPythonExclusive = False


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} running on {len(bot.guilds)} servers\n')
    logging.info(f'Logged in as {bot.user.name} running on {len(bot.guilds)} servers')

    for g in bot.guilds:
        logging.info(g.name + ' member_count: ' + str(g.member_count))

@bot.command(hidden=True)
@commands.is_owner()
async def reloadExt(ctx: commands.Context):
    '''Reloads the bot extensions without rebooting the entire program'''
    await deleteMessage(ctx)

    try:
        for ext in extensions:
            bot.reload_extension(ext)

        if not 'PyPy' in sys.version and loadPythonExclusive:
            for ext in pythonExclusiveExtensions:
                bot.reload_extension(ext)
    except:
        await ctx.send('Reloading failed')
        raise

    print('\033[94mReloading successfully finished!\033[0m\n')

@bot.command(hidden=True)
@commands.is_owner()
async def logout(ctx: commands.Context):
    await deleteMessage(ctx)
    logging.info('\nlogging out...')
    await bot.logout()

class NoParsingFilter(logging.Filter):
    def filter(self, record):
        return 'root' == record.name

if __name__ == "__main__":
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    path = pathlib.Path(__file__).parent.absolute()
    handler = logging.FileHandler(path / 'logs' / 'latest.log', 'a', 'utf-8')
    handler.setFormatter(logging.Formatter('%(name)s %(message)s'))
    handler.addFilter(NoParsingFilter())
    root_logger.addHandler(handler)
    
    for ext in extensions:
        bot.load_extension(ext)

    if not 'PyPy' in sys.version and loadPythonExclusive:
        for ext in pythonExclusiveExtensions:
            bot.load_extension(ext)
    else:
        print("Some cogs hasn't been loaded")

    bot.run(token)