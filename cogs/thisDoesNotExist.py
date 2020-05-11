import discord
from discord.ext import commands

import random
from cogs.utils.sendEmbed import sendEmbed

class AIGeneratedImg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['anime', 'neet'])
    async def waifu(self, ctx, seed: int=None):
        """quality/diversity: ~50000: mq/md, ~75000 hq/ld, ~100000 lq/hd"""
        if not seed:
            seed = random.randint(0, 199999)

        if seed < 0 or seed > 199999:
            await ctx.send('Give me a seed between 0 and 199999 inclusively!')
            return

        url = f'https://thiswaifudoesnotexist.net/v2/example-{seed}.jpg'
        await sendEmbed(ctx, url, description=f'seed: {seed}')

    @commands.command(aliases=['yiff', 'fursona'])
    async def furry(self, ctx, seed: int=None):
        """Send AI generated image from thisfursonadoesnotexist.com"""
        if not seed:
            seed = random.randint(10000, 99999)

        if seed < 10000 or seed > 99999:
            await ctx.send('Give me a valid 5-digits seed!')
            return

        url = f'https://thisfursonadoesnotexist.com/v2/jpgs-2x/seed{seed}.jpg'
        await sendEmbed(ctx, url, description=f'seed: {seed}')

def setup(bot):
    bot.add_cog(AIGeneratedImg(bot))