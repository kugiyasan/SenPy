import discord
from discord.ext import commands

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['loli'])
    async def legalize(self, ctx, age):
        try:
            age = int(age)
            if age < 1:
                raise ValueError
        except:
            await ctx.send("Give me a valid age, or else the FBI will come to your house!")
            return

        if age < 4:
            await ctx.send("Rip dude, I can't legalize your loli, get ready to get caught!")
            return 
        if age < 6:
            await ctx.send(f"{age}? That's just 10{age%2}, in base 2!")
            return 

        await ctx.send(f"{age}? That's {20+age%2}, in base {age//2}!")
        if age > 20:
            await ctx.send("But what's the purpose of legalizing already legal lolis??")

def setup(bot):
    bot.add_cog(Memes(bot))
