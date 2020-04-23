import discord
from discord.ext import commands

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx: commands.Context):
        vc = ctx.author.voice
        print(vc)
        print(vc.channel)
        if vc.channel != None:
            await vc.channel.connect()

    @commands.command()
    async def bye(self, ctx):
        await self.bot.VoiceClient.disconnect()
        commands.Bot.voice_clients

    @commands.command()
    async def play(self, ctx, *args):
        pass

def setup(bot):
    bot.add_cog(Dev(bot))