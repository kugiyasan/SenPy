import discord
from discord.ext import commands

import datetime

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    # @commands.Cog.listener()
    # async def on_typing(self, channel, user, when):
    #     if datetime.datetime.utcnow() - when > datetime.timedelta(seconds=10):
    #         await channel.send("I see that you are a slow typer, my friend")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        # if message.author == self.bot:
        #     return
        if len(message.content) > 100:
            await message.channel.send(f'{message.content[:20]}... too looooooonnnggg')

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return
        if message.content.startswith(self.bot.command_prefix):
            return
        await message.channel.send(f'Deleting your message... smh "{message.content}"')

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
                await channel.send("""Traceback (most recent call last):
                    File "events.py", line 49, in on_member_unban
                    Error: Felix never unban someone""")
                # await channel.send(err)

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        diff = set(after).difference(set(before))
        if diff:
            channels = guild.channels
            for channel in channels:
                if channel.name == 'general':
                    await channel.send('**NEW EMOJIS**' + ' '.join(map(lambda x:x.name, diff)))
                    break

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member

def setup(bot):
    bot.add_cog(Events(bot))