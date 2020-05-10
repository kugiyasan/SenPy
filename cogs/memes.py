import discord
from discord.ext import commands

import requests

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def insult(self, ctx, *, member: discord.Member = None):
        """random compliment from the web"""
        url = 'http://www.robietherobot.com/insult-generator.htm'
        webpage = requests.get(url)
        if(webpage.status_code == 200):
            w = str(webpage.content)[5862:]
            insultText = w[:w.index('<')].strip()
            
            if not member:
                await ctx.send("You're a " + insultText)
            else:
                await ctx.send(str(member) + " is a " + insultText)
        else:
            print('Error not the good status code 200 !=', webpage.status_code)

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
