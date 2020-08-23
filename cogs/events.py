import discord
from discord.ext import commands

import asyncio
import random
import re
import traceback

from cogs.utils.dbms import conn, cursor


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user or message.author.bot:
            return

        ctx = message.channel

        try:
            msgs = await ctx.history(limit=3).flatten()

            msgSet = set(m.content.lower() for m in msgs)
            authors = set(m.author for m in msgs if not m.author.bot)

            if len(msgSet) == 1 and len(authors) == 3:
                await ctx.send(msgSet.pop())
        except:
            pass

        # TODO check in the db if the server enabled those features

        # dabs = ('dab', 'DAB', '<0/', r'\0>', '<0/   <0/   <0/')
        # if re.search("|".join(dabs), message.content.lower()):
        #     style = '*' * random.randint(0, 3)
        #     await ctx.send(style + random.choice(dabs) + style)

        # if message.guild:
        #     dash = message.guild.get_member(399705801717186571)
        #     if ('rekt' in message.content.lower()
        #         and not message.author.bot
        #             and (not dash or dash.status != discord.Status.online)):
        #         await ctx.send('Yeah get rekt, son!')

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, exception):
        if (not ctx.command
            or type(exception) == asyncio.TimeoutError
                or type(exception) == commands.errors.NotOwner):
            return
        if (type(exception) == commands.errors.MissingRequiredArgument
                or type(exception) == commands.errors.BadArgument):
            await ctx.send(exception)
            await ctx.send_help(ctx.command)
            return
        if (type(exception) == commands.errors.NSFWChannelRequired
                or type(exception) == commands.errors.MissingPermissions
                or type(exception) == commands.errors.NoPrivateMessage):
            await ctx.send(exception)
            return

        print('Ignoring exception in command {}:'.format(ctx.command))
        traceback.print_exception(
            type(exception), exception, exception.__traceback__)

        await ctx.send("There was an unexpected error, I'll inform the bot dev, sorry for the incovenience")

        guild = ""
        if ctx.guild:
            guild = f"from {ctx.guild.name} "

        owner = (await self.bot.application_info()).owner
        text = (f"{ctx.author} {guild}raised an error with the command ***{ctx.command}***\n"
                + f"{type(exception)}\n{exception}"
                + "```" + "".join(traceback.format_tb(exception.__traceback__)) + "```")
        await owner.send(text)

    @ commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user):
        users = await reaction.users().flatten()
        if len(users) < 3 or any(user.bot for user in users):
            return

        if reaction.emoji == "\U0001F44E" or reaction.emoji == '⬇️':  # thumbs down
            return

        await reaction.message.add_reaction(reaction)

    @ commands.Cog.listener()
    async def on_member_join(self, member):
        channel = await self.getGeneralchannel(member.guild)
        if channel:
            await channel.send(f'おかえりなのじゃ　Okaeri nanojya {member.mention}!')

    @ commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = await self.getGeneralchannel(member.guild)
        if channel:
            await channel.send(f'See you later alligator {member.mention}.')

    @ commands.Cog.listener()
    async def on_guild_emojis_update(self, guild: discord.Guild, before, after):
        diff = set(after).difference(set(before))
        if diff:
            channel = await self.getGeneralchannel(guild)

            await channel.send('**NEW EMOJIS**')
            newemojis = ' '.join(map(lambda x: str(x), diff))
            await channel.send(newemojis)

    async def getGeneralchannel(self, guild: discord.Guild):
        with conn:
            cursor.execute(
                "SELECT welcomebye FROM guilds WHERE id=%s", (guild.id,))
            return self.bot.get_channel(cursor.fetchone()[0])


def setup(bot: commands.Bot):
    bot.add_cog(Events(bot))
