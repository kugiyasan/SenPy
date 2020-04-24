import discord
from discord.ext import commands

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx: commands.Context):
        vc = ctx.author.voice
        print(vc.channel)
        voice_clients = self.bot.voice_clients
        if voice_clients:
            print(voice_clients[0])
        if vc.channel != None:
            await vc.channel.connect()

    @commands.command()
    async def cursed(self, ctx):
        vc = self.bot.voice_clients
        if len(vc):
            vc[0].play(discord.PCMAudio(open('audio.wav', 'rb')))

    @commands.command(aliases=['paly', 'queue', 'que'])
    async def play(self, ctx):
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        audio_source = discord.FFmpegPCMAudio('audio.mp3')
        if not voice_client.is_playing():
            voice_client.play(audio_source)

    @commands.command()
    async def pause(self, ctx, *args):
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client.is_playing():
            voice_client.pause()

    @commands.command()
    async def resume(self, ctx, *args):
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if not voice_client.is_playing():
            voice_client.resume()

    @commands.command()
    async def disconnect(self, ctx, *args):
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client:
            voice_client.disconnect()

    @commands.command()
    async def stop(self, ctx, *args):
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client.is_playing():
            voice_client.stop()

def setup(bot):
    bot.add_cog(Voice(bot))