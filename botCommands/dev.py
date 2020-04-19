# import discord
# from discord.ext import commands

# class Dev(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot

#     @commands.command()
#     @commands.is_owner()
#     async def reloadExt(self, ctx):
#         """reload the commands to make it faster and easier to apply changes"""
#         for ext in extensions:
#             bot.reload_extension(ext)

#     @commands.command()
#     @commands.is_owner()
#     async def stop(self, ctx):
#         """DON'T"""
#         print('\nlogging out...')
#         await bot.logout()

def setup(bot):
    pass
    # bot.add_cog(Dev(bot))