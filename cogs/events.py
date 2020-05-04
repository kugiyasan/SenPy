import discord
from discord.ext import commands

import logging
import random

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # message.delete() # rampage mode
        if message.author == self.bot.user:
            return
        guildChannel = ' '
        if message.guild != None:
            guildChannel = ' ' + message.guild.name + ' #' + str(message.channel) + ' '
        timename = str(message.created_at)[:-3] + ' ' + message.author.name
        logging.info(timename + guildChannel + message.content)
        
        ctx = message.channel
        
        codingChannel = 693920225846100049
        if '```' in message.content and message.guild.name == 'Banana Squad' and message.channel.id != codingChannel:
            await ctx.send(f'Coding goes into #{codingChannel}')

        dabs = ['dab', 'DAB', '<0/', r'\0>', '<0/   <0/   <0/']
        for dab in dabs:
            if dab in message.content.split():
                style = random.randint(0, 3)
                wrapper = '*'*style + '{}' + '*'*style
                await ctx.send(wrapper.format(random.choice(dabs)))

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
    async def on_guild_emojis_update(self, guild, before, after):
        diff = set(after).difference(set(before))
        if diff:
            channels = guild.channels
            for channel in channels:
                if channel.name == 'general':
                    newemojis = ' '.join(map(lambda x:x.name, diff))
                    await channel.send('**NEW EMOJIS**' + newemojis)
                    break

def setup(bot):
    bot.add_cog(Events(bot))