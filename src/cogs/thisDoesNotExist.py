import discord
from discord.ext import commands

import random
from pathlib import Path

from cogs.mofupoints import incrementEmbedCounter
from cogs.utils.sendEmbed import sendEmbed


class AIGeneratedImg(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["anime", "neet", "speedwagon"])
    async def waifu(self, ctx: commands.Context, seed=None):
        """quality/diversity: ~50000: mq/md, ~75000 hq/ld, ~100000 lq/hd"""
        url = "https://thiswaifudoesnotexist.net/v2/example-{}.jpg"
        await self.sendAIImg(ctx, url, seed, 0, 199999)

    @commands.command(aliases=["yiff", "fursona"])
    async def furry(self, ctx: commands.Context, seed=None):
        """Send AI generated image from thisfursonadoesnotexist.com"""
        url = "https://thisfursonadoesnotexist.com/v2/jpgs-2x/seed{}.jpg"
        await self.sendAIImg(ctx, url, seed, 0, 99999)

    async def sendAIImg(
        self, ctx: commands.Context, url: str, seed: int, seedmin: int, seedmax: int
    ):
        if seed is None:
            seed = random.randint(seedmin, seedmax)
        else:
            try:
                seed = int(seed)
            except ValueError:
                await ctx.send("The seed isn't a number!")
                return

        if seed < seedmin or seed > seedmax:
            err = f"Give me a seed between {seedmin} and {seedmax} inclusively!"
            await ctx.send(err)
            return

        await sendEmbed(ctx, url.format(seed), description=f"seed: {seed}")

    @commands.command(hidden=True)
    async def husbando(self, ctx: commands.Context, seed: int = None):
        """AI generated husbandos"""
        if seed is None:
            seed = random.randint(0, 1003)

        if seed < 0 or seed > 1003:
            await ctx.send("Give me a seed between 0 and 1003 inclusively!")
            return

        img_path = (
            Path(__file__).parent.parent.parent
            / "media/2019-05-06-stylegan-malefaces-1ksamples"
        )

        number = str(seed).zfill(4)
        file = discord.File(img_path / f"{number}.jpg", filename="image.png")
        await sendEmbed(
            ctx,
            "attachment://image.png",
            localImageFile=file,
            description=f"seed: {seed}",
        )

        incrementEmbedCounter(ctx.author)


def setup(bot: commands.Bot):
    bot.add_cog(AIGeneratedImg(bot))
