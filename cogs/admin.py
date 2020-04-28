import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx, *members: discord.Member):
        """wait the bot has ban permission?!?"""
        output = ', '.join(m.name for m in members)
        await ctx.send(f'''`{output} has been banned from the server...
                        just kidding I can\'t do that`''')

    @commands.command()
    async def delete(self, ctx: commands.Context):
        """delete the last message of the bot"""
        await ctx.message.delete()

        async for message in ctx.history():
            #TODO should only delete his own messsage
            if message.author.bot:
                await message.delete()
                break
            

def setup(bot):
    bot.add_cog(Admin(bot))