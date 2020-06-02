import discord
from discord.ext import commands

# import deeppyer

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        pass
        # print(discord.Permissions.send_messages)

    @commands.command()
    async def test(self, ctx: commands.Context):
        file = discord.File("media/hanamaru.jpg", filename="image.png")
        embed = discord.Embed()
        embed.set_image(url="attachment://image.png")
        await ctx.send(file=file, embed=embed)

    @commands.command()
    async def deepfry(self, ctx: commands.Context):
        pass

def setup(bot):
    bot.add_cog(Dev(bot))

