import discord
from discord.ext import commands

import asyncio
from time import time

#TODO auto disconnect bot after 5 minutes

# def autoDisconnect(func):
#     async def inner(self, ctx):
#         currentTime = time()
#         self.lastCommandTime[ctx.guild] = currentTime

#         await func(self, ctx)
        
#         await asyncio.sleep(10)
#         if self.lastCommandTime[ctx.guild] == currentTime:
#             await self.disconnect(ctx)
#     return inner

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lastCommandTime = {}
        self.looping = False

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after: discord.VoiceState):
        if not after.channel:
            # someone quit the vc
            for voice_channel in member.guild.voice_channels:
                if voice_channel.members == []:
                    continue
                for member in voice_channel.members:
                    if not member.bot:
                        break
                else:
                    await self.disconnect(member)
                    break

    #! should async (can't bc self.getvc)
    def getvc(self, ctx):
        return discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

    @commands.command()
    async def join(self, ctx: commands.Context):
        self.lastCommandTime[ctx.guild] = time()
        vc = ctx.author.voice
        voice_client: discord.VoiceClient = self.getvc(ctx)
        
        if voice_client and voice_client.is_connected():
            await voice_client.move_to(vc.channel)

        if vc.channel != None:
            await vc.channel.connect()
            voice_client = self.getvc(ctx)
        else:
            await ctx.send('get into a voice channel so I can join!')
            return

        voice_client.play(discord.FFmpegOpusAudio('media/welcome.mp3'))
        while voice_client.is_playing():
            asyncio.sleep(0.1)

    @commands.command()
    async def cursed(self, ctx):
        '''ok this command is going to be here for a bit more'''
        '''Please Buramie let me delete this shit'''
        voice_client: discord.VoiceClient = self.getvc(ctx)
        audio_source = discord.PCMAudio(open('media/audio.wav', 'rb'))
        
        if not voice_client:
            await self.join(ctx)
            voice_client: discord.VoiceClient = self.getvc(ctx)

        if not voice_client.is_playing():
            if ctx.author.name == 'Buramie':
                await ctx.send('Pls don\'t start the song...')
                return
            voice_client.play(audio_source)

    @commands.command(aliases=['paly', 'queue', 'que', 'p'])
    async def play(self, ctx):
        '''Play the senko-san opening!'''
        voice_client: discord.VoiceClient = self.getvc(ctx)
        audio_source = discord.FFmpegOpusAudio('media/audio.mp3')

        if not voice_client:
            await self.join(ctx)
            voice_client: discord.VoiceClient = self.getvc(ctx)

        if not voice_client.is_playing():
            voice_client.play(audio_source)

    @commands.command(aliases=['infinity'])
    async def loop(self, ctx):
        '''Infinite senko op!'''
        self.looping = True
        while self.looping:
            await self.play(ctx)
                    
            await asyncio.sleep(1)

    @commands.command(aliases=['rev'])
    async def reverse(self, ctx):
        '''!gninepo nas-oknes eht yalP'''
        voice_client: discord.VoiceClient = self.getvc(ctx)
        audio_source = discord.FFmpegOpusAudio('media/reversedAudio.mp3')

        if not voice_client:
            await self.join(ctx)
            voice_client: discord.VoiceClient = self.getvc(ctx)

        if not voice_client.is_playing():
            voice_client.play(audio_source)

    @commands.command()
    async def pause(self, ctx, *args):
        self.looping = False

        voice_client: discord.VoiceClient = self.getvc(ctx)
        if voice_client.is_playing():
            voice_client.pause()

    @commands.command()
    async def resume(self, ctx, *args):
        voice_client: discord.VoiceClient = self.getvc(ctx)
        if voice_client.is_paused():
            voice_client.resume()

    @commands.command()
    async def stop(self, ctx, *args):
        self.looping = False

        voice_client: discord.VoiceClient = self.getvc(ctx)
        if voice_client.is_playing():
            voice_client.stop()

    @commands.command(aliases=['bye'])
    async def disconnect(self, ctx, *args):
        await self.stop(ctx)

        voice_client: discord.VoiceClient = self.getvc(ctx)
        if voice_client:
            voice_client.play(discord.FFmpegOpusAudio('media/seeya.mp3'))
            while voice_client.is_playing():
                asyncio.sleep(0.1)

            await voice_client.disconnect()

def setup(bot):
    bot.add_cog(Voice(bot))