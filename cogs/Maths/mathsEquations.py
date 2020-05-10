import discord
from discord.ext import commands

class MathsEquations(commands.Cog, name='Maths'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['slope'])
    async def function_analytic(self, ctx, x1: float, x2: float, y1: float, y2: float):
        slope = (y1 - y2) / (x1 - x2)
        b = y1 - slope * x1
        await ctx.send("y = {:.5g} x + {:.5g}".format(slope, b))

    @commands.command(aliases=['pythagoras'])
    async def pythagorean_theorem(self, ctx, cathetus: float, hypothesis: float):
        await ctx.send('|\\\n|   \\ <--Hypothesis\n|      \\\n|_____\\')
        await ctx.send((cathetus**2 - hypothesis**2) ** 0.5)

    @commands.command(aliases=['pythagoras2'])
    async def pythagorean_theorem2(self, ctx, cathetus1: float, cathetus2: float):
        await ctx.send('|\\\n|   \\ <--Hypothesis\n|      \\\n|_____\\')
        await ctx.send((cathetus1**2 + cathetus2**2) ** 0.5)

    @commands.command(aliases=['heron'])
    async def herons_formula(self, ctx, a: float, b: float, c:float):  
        p = (a + b + c) / 2
        await ctx.send((p * (p - a) * (p - b) * (p - c)) ** 0.5)

    @commands.command(aliases=['quad', 'quadratic'])
    async def vietas_formulas(self, ctx, a: float, b: float, c: float):
        await ctx.send("ax² + bx + c = 0")
        half = -b / a / 2
        u = (half**2 - c) ** 0.5
        x1 = half - u
        x2 = half + u
        await ctx.send("x1= {:.5g} x2= {:.5g}".format(x1, x2))
            
    @commands.command()
    async def prime_number_detector(self, ctx, n: int):
        y = True
        for x in range(2, int(n**0.5 + 1)):
            if n % x == 0:
                if y:
                    await ctx.send(f"{n} is equal to:")
                    y = False
                await ctx.send(f"{x} * {n//x}")
        if y:
            await ctx.send(f"{n} is a prime number")

    @commands.command()
    async def prime_number(self, ctx, n: int):
        for x in range(2, n-1):
            while n % x == 0:
                await ctx.send(f"{n} is not a prime number")
                await ctx.send(f"{x} * {n//x} is {n}")
                n //= x
                break
        else:
            await ctx.send(f"{n} is a prime number")

    @commands.command()
    async def factors(self, ctx, n: int):
        while n % 2 == 0:
            await ctx.send(2)
            n = n // 2
        for i in range(3, int(n**0.5) + 1, 2):
            while n % i == 0:
                await ctx.send (i)
                n = n // i
        if n > 2:
            await ctx.send(n)

def setup(bot):
    bot.add_cog(MathsEquations(bot))