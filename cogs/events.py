import discord
from discord.ext import commands

import random
import re
import traceback

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        ctx = message.channel
        
        # if not ctx.permissions_for(ctx.guild.get_member(self.bot.user.id)).manage_messages:
        #     await ctx.send("Can't edit messages")
        #     return

        dabs = ['dab', 'DAB', '<0/', r'\0>', '<0/   <0/   <0/']
        for dab in dabs:
            if dab in message.content.lower().split():
                style = '*' * random.randint(0, 3)
                wrapper = style + '{}' + style
                await ctx.send(wrapper.format(random.choice(dabs)))

        if message.guild:
            dash = message.guild.get_member(399705801717186571)
            if ('rekt' in message.content.lower()
                and not message.author.bot
                    and (not dash or dash.status != discord.Status.online)):
                await ctx.send('Yeah get rekt, son!')

        try:
            msgs = await ctx.history(limit=3).flatten()

            msgSet = set(m.content for m in msgs)
            authors = set(m.author for m in msgs if not m.author.bot)

            if len(msgSet) == 1 and len(authors) == 3:
                await ctx.send(msgSet.pop())
        except:
            pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, exception):
        if not ctx.command:
            return
        if type(exception) == commands.errors.MissingRequiredArgument:
            await ctx.send(exception)
            await ctx.send_help(ctx.command)
            return

        print('Ignoring exception in command {}:'.format(ctx.command))
        traceback.print_exception(type(exception), exception, exception.__traceback__)

        await ctx.send("There was an unexpected error, I'll inform the bot dev, sorry for the incovenience")

        channel = await self.bot.get_user(self.bot.owner_id).create_dm()
        text = (f"{ctx.author} raised an error with the command ***{ctx.command}***\n"
                + f"{type(exception)}\n{exception}"
                + "```" + "".join(traceback.format_tb(exception.__traceback__)) + "```")
        await channel.send(text)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user):
        users = await reaction.users().flatten()
        if len(users) == 1 and users[0].bot:
            return

        if reaction.emoji == "\U0001F44E" or reaction.emoji == '⬇️':  # thumbs down
            return

        await reaction.message.add_reaction(reaction)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = await self.getGeneralchannel(member.guild)
        await channel.send(f'おかえりなのじゃ　Okaeri nanojya {member.mention}!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = await self.getGeneralchannel(member.guild)
        await channel.send(f'See you later alligator {member.mention}.')

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        channel = await self.getGeneralchannel(guild)
        await channel.send(f"{guild.owner.name} used Banhammer!\nIt's super effective!")

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        channel = await self.getGeneralchannel(guild)
        await channel.send(f"""Traceback (most recent call last):
            File "events.py", line 110, in on_member_unban
            Error: {guild.owner.name} never unban someone""")

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild: discord.Guild, before, after):
        diff = set(after).difference(set(before))
        if diff:
            channel = await self.getGeneralchannel(guild)

            await channel.send('**NEW EMOJIS**')
            newemojis = ' '.join(map(lambda x: str(x), diff))
            await channel.send(newemojis)

    async def getGeneralchannel(self, guild: discord.Guild):
        botMember = guild.get_member(self.bot.user.id)
        async for channel in self.channelGenerator(guild):
            if (channel != None
                    and channel.permissions_for(botMember).send_messages):
                return channel

    async def channelGenerator(self, guild):
        yield guild.system_channel

        for channel in guild.channels:
            if 'welcome' in channel.name.lower():
                yield channel
            elif re.search('g[eé]n[eé]ral', channel.name):
                yield channel

        for channel in guild.channels:
            yield channel

        raise self.NoWritableChannelError

    class NoWritableChannelError(Exception):
        pass


def setup(bot):
    bot.add_cog(Events(bot))
