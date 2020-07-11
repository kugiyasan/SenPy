# https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html
# https://github.com/runarsf/rufus

import discord
from discord.ext import commands

import sys

from cogs.utils.embedPaginator import EmbedHelpCommand, EmbedPaginator
from cogs.utils.deleteMessage import deleteMessage
from cogs.utils.dbms import conn

from discordToken import token


async def prefixes(bot: commands.Bot, message: discord.Message):
    prefix = "xd"
    if message.guild != None:
        with conn:
            temp = conn.execute("SELECT command_prefix FROM guilds WHERE id = ?", (message.guild.id,)).fetchone()
            if temp:
                prefix = temp[0]

    return commands.when_mentioned_or(prefix + " ", prefix)(bot, message)

description = '''Senko-san wants to pamper you'''

bot = commands.Bot(command_prefix=prefixes,
                   description=description,
                #    help_command=commands.DefaultHelpCommand())
                   help_command=EmbedHelpCommand(paginator=EmbedPaginator()))

extensions = ('cogs.Games.chessCog',
              'cogs.Games.mastermind',
              'cogs.Games.russianRoulette',
              'cogs.admin',
              'cogs.dev',
              'cogs.events',
              'cogs.info',
              'cogs.memes',
              'cogs.mofupoints',
              'cogs.neko',
              'cogs.reddit',
              'cogs.thisDoesNotExist')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Running on {len(bot.guilds)} servers\n')

    for g in bot.guilds:
        print(g.name + ' member_count: ' + str(g.member_count))


@bot.command(hidden=True)
@commands.is_owner()
async def reload(ctx: commands.Context):
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
