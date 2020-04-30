import discord
from discord.ext import commands

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def getvc(self, ctx):
        return discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

    @commands.command()
    async def join(self, ctx: commands.Context):
        vc = ctx.author.voice
        # print(vc.channel)
        voice_client: discord.VoiceClient = self.getvc(ctx)
        if voice_client and voice_client.is_connected():
            await voice_client.move_to(vc.channel)
            return
        if vc.channel != None:
            await vc.channel.connect()
        else:
            await ctx.send('get into a voice channel so I can join!')

    @commands.command()
    async def cursed(self, ctx):
        '''Please Buramie let me delete this shit'''
        voice_client: discord.VoiceClient = self.getvc(ctx)
        audio_source = discord.PCMAudio(open('media/audio.wav', 'rb'))
        if not voice_client:
            await self.join(ctx)
            voice_client: discord.VoiceClient = self.getvc(ctx)
        if not voice_client.is_playing():
            voice_client.play(audio_source)

    @commands.command(aliases=['paly', 'queue', 'que', 'p'])
    async def play(self, ctx):
        '''Play the senko-san opening!'''
        voice_client: discord.VoiceClient = self.getvc(ctx)
        audio_source = discord.FFmpegPCMAudio('media/audio.mp3')
        if not voice_client:
            await self.join(ctx)
            voice_client: discord.VoiceClient = self.getvc(ctx)
        if not voice_client.is_playing():
            voice_client.play(audio_source)

    @commands.command()
    async def pause(self, ctx, *args):
        voice_client: discord.VoiceClient = self.getvc(ctx)
        if voice_client.is_playing():
            voice_client.pause()

    @commands.command()
    async def resume(self, ctx, *args):
        voice_client: discord.VoiceClient = self.getvc(ctx)
        if voice_client.is_paused():
            voice_client.resume()

    @commands.command(aliases=['bye'])
    async def disconnect(self, ctx, *args):
        voice_client: discord.VoiceClient = self.getvc(ctx)
        if voice_client:
            await voice_client.disconnect()

def setup(bot):
    bot.add_cog(Voice(bot))