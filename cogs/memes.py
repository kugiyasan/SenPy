import discord
from discord.ext import commands

from lxml import html
import requests

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.someoneEnabled = False

    @commands.command()
    async def insult(self, ctx, *, member: discord.Member = None):
        """random compliment from the web (robietherobot.com/insult-generator.htm)"""
        url = "http://www.robietherobot.com/insult-generator.htm"
        webpage = requests.get(url)
        if(webpage.status_code == 200):
            tree = html.fromstring(webpage.content)
            insultText = tree.xpath("//h1")[1].text.strip()

            if not member:
                await ctx.send("You're a " + insultText)
            else:
                await ctx.send(str(member) + " is a " + insultText)
        else:
            print("Error not the good status code 200 !=", webpage.status_code)
            raise ConnectionError

    @commands.command(aliases=["legal"])
    async def legalize(self, ctx, age):
        """All lolis can be legal, if you let me handle it!"""
        try:
            age = int(age)
            if age < 1:
                raise ValueError
        except ValueError:
            await ctx.send("Give me a valid age, or else the FBI will come to your house!")
            return

        if age < 4:
            await ctx.send("Rip dude, I can't legalize your loli, get ready to be caught!")
        elif age < 6:
            await ctx.send(f"{age}? That's just 10{age%2}, in base 2!")
        elif age > 20:
            await ctx.send("But what's the purpose of legalizing already legal lolis??")
        else:
            await ctx.send(f"{age}? That's {20+age%2}, in base {age//2}!")

    @commands.command(aliases=["cat"])
    async def catyears(self, ctx, age):
        """The following program does not endorse in any way, shape or form the slavery of sapient beings"""
        try:
            age = int(age)
            if age < 1:
                raise ValueError
        except:
            await ctx.send("As far as I can tell, it is impossible to have a relationship with a being that does not exist (yet). However, a legend says some mythical man once succeded in this seemingly unachievable feat, through his infinite love for a certain heterochromatic nekomimi...")
            return

        if age == 1:
            await ctx.send('Hmm, while there have been no scientific consensus as of yet, your cat seems to be... 12.5 years old. To safely engage in intercourse, you would need to say \"no beasto\" and \"no pedo\" at the same time, which is sadly not physically possible. I advise you wait just a few months before indulging in your deep fantasies.')
        elif age == 2:
            await ctx.send('Hmm. Your cat has finished its initial growth stage, bringing them to the very mature age of 25 years old. Your patience has been justly rewarded. You may... proceed. Remember to say \"no beasto\", though.')
        elif age > 20:
            await ctx.send(f"What? Your cat is already {age}? That means... they are now {25+(age-2)*4}, in human years! Although... a doubt still plagues my mind. Are you sure that your cat is still alive and well? They should be deceased by now, according to statistical evidence. I'd be cautious if I were you. Saying \"no beasto\" and \"no necro\" at the same time is sadly not physically possible.")
        else:
            await ctx.send(f"What? Your cat is already {age}? That means... they are now {25+(age-2)*4}, in human years! Make haste, before death does you part! I know these beings are... disposable, but that is not a good reason to leave them decay, untouched by your love.")


def setup(bot: commands.Bot):
    bot.add_cog(Memes(bot))
