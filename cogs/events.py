import discord
from discord.ext import commands

from datetime import datetime
from dateutil import tz

import asyncio
import logging
import random
import re

async def utc2localTime(utc):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    # Tell the datetime object that it's in UTC time zone since 
    # datetime objects are 'naive' by default
    utc = utc.replace(tzinfo=from_zone)

    # Convert time zone
    central = utc.astimezone(to_zone)
    
    return str(central)[:-9]

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # message.delete() # rampage mode
        if message.author == self.bot.user:
            return

        guildChannel = ''
        if message.guild != None:
            guildChannel = message.guild.name + ' #' + str(message.channel)
        time = await utc2localTime(message.created_at)
        logging.info(' '.join((time, message.author.name, guildChannel, message.content)))

        ctx = message.channel
        
        codingChannel = 693920225846100049
        if ('```' in message.content 
            and message.guild.name == 'Banana Squad' 
            and message.channel.id != codingChannel):
            await ctx.send(f'Coding goes into <#{codingChannel}>')

        dabs = ['dab', 'DAB', '<0/', r'\0>', '<0/   <0/   <0/']
        for dab in dabs:
            if dab in message.content.lower().split():
                style = random.randint(0, 3)
                wrapper = '*'*style + '{}' + '*'*style
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
    async def on_reaction_add(self, reaction: discord.Reaction, user):
        users = await reaction.users().flatten()
        if len(users) == 1 and users[0].bot:
            return

        if reaction.emoji == "\U0001F44E" or reaction.emoji == '⬇️': #thumbs down
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