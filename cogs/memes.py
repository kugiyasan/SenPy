import discord
from discord.ext import commands

from lxml import html
from PIL import Image
import deeppyer
import requests
from io import BytesIO

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def insult(self, ctx, *, member: discord.Member = None):
        """random compliment from the web"""
        url = 'http://www.robietherobot.com/insult-generator.htm'
        webpage = requests.get(url)
        if(webpage.status_code == 200):
            tree = html.fromstring(webpage.content)
            insultText = tree.xpath('//h1')[1].text.strip()
            
            if not member:
                await ctx.send("You're a " + insultText)
            else:
                await ctx.send(str(member) + " is a " + insultText)
        else:
            print('Error not the good status code 200 !=', webpage.status_code)

    @commands.command(aliases=['loli'])
    async def legalize(self, ctx, age):
        '''All lolis can be legal, if you let me handle it!'''
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

    @commands.command(aliases=['df'])
    async def deepfry(self, ctx: commands.Context):
        '''haha image goes brrrrrrrr'''

        if not ctx.message.attachments:
            await ctx.send('Please attach an image!')
            return
            
        # PATH = f'media/deepfry_{ctx.author.name}.png'
        file = await ctx.message.attachments[0].read()
        # print(file)
        img = Image.open(BytesIO(file))
        img = await deeppyer.deepfry(img)# , flares=False)

        # imgBytes = io.BytesIO()
        # img.save(imgBytes, format='PNG')
        # imgBytes = imgBytes.getvalue()

        # toSend = discord.File(io.BytesIO(imgBytes), filename=f'deepfry_{ctx.author.name}.png')
        toSend = discord.File(Image.open(img))
        await ctx.send(file=toSend)


def setup(bot):
    bot.add_cog(Memes(bot))
