import discord
from discord.ext import commands

import datetime
import random

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_typing(self, channel, user, when):
    #     if datetime.datetime.utcnow() - when > datetime.timedelta(seconds=10):
    #         await channel.send("I see that you are a slow typer, my friend")
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # message.delete() # rampage mode
        if message.author.bot: #or self.bot.owner_id == message.author:
            return
        if message.guild != None:
            print(message.guild.name, f'#{message.channel}')
        timename = str(message.created_at) + message.author.name
        print(timename, '\033[32m', message.content, ' \033[0m')
        dabs = ['dab', 'DAB', '<0/', '<0/', r'\0>', '<0/   <0/   <0/']
        for dab in dabs:
            if dab in message.content:
                wrapper = '{}'
                if random.randint(0, 1):
                    wrapper = '**{}**'
                await message.channel.send(wrapper.format(random.choice(dabs)))

        # #! the long message troll wasn't removed like asked gottem
        # m = message.content
        # if len(m) > 1000:
        #     await message.channel.send(f'{m[:20]}... too looooooonnnnnngggg')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        await reaction.message.add_reaction(reaction)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'See you later aligator {member.mention}.')

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        channel = guild.system_channel
        if channel is not None:
            await channel.send("Félix used Banhammer!\nIt's super effective!") 
            
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
                    Error: Felix never unban someone""")
                
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