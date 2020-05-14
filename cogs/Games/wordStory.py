import discord
from discord.ext import commands

import json
import random
from cogs.utils.configJson import updateWordStory, getValueJson

class WordStory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        with open('config.json', 'r') as configFile:
            try:
                guild = json.load(configFile)['guilds'][message.guild.name]
                channel_id = guild['word-story']['channel_id']
            except:
                return

            if channel_id == message.channel.id:
                msg = message.content
                
                if '*' in msg:
                    msg = msg[:message.content.index('*')]
                if '[' in msg:
                    msg = msg[:message.content.index('[')]
                
                if guild['command_prefix'] in msg.lower():
                    return

                await updateWordStory(msg.strip(),
                                    message.guild.name, 'story',
                                    appendList=True)

                currentLength = len(guild['word-story']['story'])
                #* should send only if it is wrong
                # await message.channel.send(f'[{currentLength}]')
                await message.add_reaction(self.bot.get_emoji(645461243712503848))

                if guild['word-story']['maxLength'] <= currentLength:
                    await finishStory(message.channel, message.content)
    
    @commands.command(aliases=['finishstory'])
    @commands.has_permissions(administrator=True)
    async def finishStory(self, ctx, lastMessage=None):
        story = await getValueJson('guilds', ctx.guild.name, 'word-story', 'story')
        story = story[1:]
        if lastMessage:
            story.append(lastMessage)

        await ctx.send('The story is finished!')
        await ctx.send(' '.join(story))

        await updateWordStory([], ctx.guild.name, 'story')

    @commands.command(aliases=['newstory'])
    @commands.has_permissions(administrator=True)
    async def newStory(self, ctx: commands.Context, storyLength=50):
        """Start a word story in a channel"""
        await updateWordStory(ctx.channel.id, ctx.guild.name, 'channel_id')
        await updateWordStory(storyLength, ctx.guild.name, 'maxLength')
        await updateWordStory([], ctx.guild.name, 'story')

        await ctx.send(f'<#{ctx.channel.id}> will be the channel for word-story on this server!')
        await ctx.send(f'The story is going to be {storyLength} words long')

def setup(bot):
    bot.add_cog(WordStory(bot))