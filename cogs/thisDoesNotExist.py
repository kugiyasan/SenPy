import discord
from discord.ext import commands

import pathlib
import random

from cogs.mofupoints import incrementEmbedCounter
from cogs.utils.sendEmbed import sendEmbed


class AIGeneratedImg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['anime', 'neet', 'speedwagon'])
    async def waifu(self, ctx, seed=None):
        """quality/diversity: ~50000: mq/md, ~75000 hq/ld, ~100000 lq/hd"""
        url = 'https://thiswaifudoesnotexist.net/v2/example-{}.jpg'
        await self.sendAIImg(ctx, url, seed, 0, 199999)

    @commands.command(aliases=['yiff', 'fursona'])
    async def furry(self, ctx, seed=None):
        """Send AI generated image from thisfursonadoesnotexist.com"""
        url = 'https://thisfursonadoesnotexist.com/v2/jpgs-2x/seed{}.jpg'
        await self.sendAIImg(ctx, url, seed, 10000, 99999)

    async def sendAIImg(self, ctx: commands.Context, url, seed, seedmin, seedmax):
        if seed is None:
            seed = random.randint(seedmin, seedmax)
        else:
            try:
                seed = int(seed)
            except ValueError:
                await ctx.send("The seed isn't a number!")
                return

        if seed < seedmin or seed > seedmax:
            await ctx.send(f'Give me a seed between {seedmin} and {seedmax} inclusively!')
            return

        await sendEmbed(ctx, url.format(seed), description=f'seed: {seed}')

    @commands.command(hidden=True)
    async def husbando(self, ctx, seed: int = None):
        """AI generated husbandos"""
        if not seed:
            seed = random.randint(0, 1003)

        if seed < 0 or seed > 1003:
            await ctx.send('Give me a seed between 0 and 1003 inclusively!')
            return

        number = str(seed).zfill(4)
        imgPath = f'media/2019-05-06-stylegan-malefaces-1ksamples/{number}.jpg'

        file = discord.File(imgPath, filename="image.png")
        await sendEmbed(ctx, "attachment://image.png", localImageFile=file, description=f'seed: {seed}')

        await incrementEmbedCounter(ctx.author)


def setup(bot):
    bot.add_cog(AIGeneratedImg(bot))
