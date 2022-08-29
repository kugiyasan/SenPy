from discord.ext import commands

import random
from typing import Optional

from .mofupoints import incrementEmbedCounter
from .utils.sendEmbed import sendEmbed


class AIGeneratedImg(commands.Cog):
    @commands.command(aliases=["anime", "neet", "speedwagon"])
    async def waifu(self, ctx: commands.Context, seed: int = None) -> None:
        """quality/diversity: ~50000: mq/md, ~75000 hq/ld, ~100000 lq/hd"""
        url = "https://thiswaifudoesnotexist.net/v2/example-{}.jpg"
        await self.sendAIImg(ctx, url, seed, 0, 199999)

    @commands.command(aliases=["yiff", "fursona"])
    async def furry(self, ctx: commands.Context, seed: int = None) -> None:
        """Send AI generated image from thisfursonadoesnotexist.com"""
        url = "https://thisfursonadoesnotexist.com/v2/jpgs-2x/seed{}.jpg"
        await self.sendAIImg(ctx, url, seed, 0, 99999)

    async def sendAIImg(
        self,
        ctx: commands.Context,
        url: str,
        seed: Optional[int],
        seedmin: int,
        seedmax: int,
    ) -> None:
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
        incrementEmbedCounter(ctx.author)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AIGeneratedImg())
