import discord
from discord.ext import commands

from datetime import datetime
from dateutil import tz

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

        dash = message.guild.get_member(399705801717186571)
        if ('rekt' in message.content.lower()
            and not message.author.bot
            and (not dash or dash.status != discord.Status.online)):
            await ctx.send('Yeah get rekt, son!')

        #* Be sure that the first message isn't from the bot
        msg1, msg2 = await ctx.history(limit=2).flatten()
        if (msg1.content == msg2.content
            and msg1.author != msg2.author):
            # and not msg1.author.bot):
            await ctx.send(msg1.content)

        # #! the long message troll wasn't removed like asked gottem
        # m = message.content
        # if len(m) > 1000:
        #     await message.channel.send(f'{m[:20]}... too looooooonnnnnngggg')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user):
        if reaction.emoji == "\U0001F44E" or reaction.emoji == '⬇️': #thumbs down
            return
        await reaction.message.add_reaction(reaction)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'おかえりなのじゃ　Okaeri nanojya {member.mention}!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'See you later alligator {member.mention}.')

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        channel = guild.system_channel
        if channel is not None:
            await channel.send("Buramie used Banhammer!\nIt's super effective!") 
            
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        channel = guild.system_channel
        if channel is not None:
            try:
                raise Exception
            except Exception as err:
                await channel.send(err)
                await channel.send("""Traceback (most recent call last):
                    File "events.py", line 49, in on_member_unban
                    Error: Buramie never unban someone""")
                
    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild: discord.Guild, before, after):
        diff = set(after).difference(set(before))
        if diff:
            channel = guild.system_channel
            try:
                await channel.send('**NEW EMOJIS**')
                newemojis = ' '.join(map(lambda x: str(x), diff))
                await channel.send(newemojis)
            except:
                for channel in guild.channels:
                    if re.search('g[eé]n[eé]ral', channel.name):
                        await channel.send('**NEW EMOJIS**')
                        newemojis = ' '.join(map(lambda x: str(x), diff))
                        await channel.send(newemojis)

def setup(bot):
    bot.add_cog(Events(bot))