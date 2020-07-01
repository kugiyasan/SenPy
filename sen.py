# https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html
# https://github.com/runarsf/rufus

import discord
from discord.ext import commands

import itertools
import sys

from cogs.utils.deleteMessage import deleteMessage
from cogs.utils.configJson import getValueJson

from discordToken import token


def variations(prefix):
    bothCase = ((c.upper(), c.lower()) for c in prefix)
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

bot = commands.Bot(command_prefix=prefixes,
                   description=description)
# bot.remove_command('help')

extensions = ('cogs.Games.chessCog',
              'cogs.Games.mastermind',
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


@bot.event
async def on_ready():
    print(
        f'Logged in as {bot.user.name} running on {len(bot.guilds)} servers\n')

    for g in bot.guilds:
        print(g.name + ' member_count: ' + str(g.member_count))


@bot.command(hidden=True)
@commands.is_owner()
async def reloadExt(ctx: commands.Context):
    '''Reloads the bot extensions without rebooting the entire program'''
    await deleteMessage(ctx)

    try:
        for ext in extensions:
            bot.reload_extension(ext)
    except:
        await ctx.send('Reloading failed')
        raise

    print('\033[94mReloading successfully finished!\033[0m\n')


@bot.command(hidden=True)
@commands.is_owner()
async def logout(ctx: commands.Context):
    await deleteMessage(ctx)
    await bot.logout()

if __name__ == "__main__":
    for ext in extensions:
        bot.load_extension(ext)

    bot.run(token)
