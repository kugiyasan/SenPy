import discord
from discord.ext import commands

import pathlib

# https://realpython.com/python-matplotlib-guide/
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# from PIL import Image
# import deeppyer

class MatPlotLib(commands.Cog, name='VisualizeData'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['plot'])
    async def classPlot(self, ctx, mean: float, stdDev: float):
        """Visualize the grade scattering of your class with just the mean and standard deviation"""
        x = np.arange(0, 100, 1)
        y2 = norm.pdf(x, mean, stdDev)

        # build the plot
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(9,6))
        ax.plot(x, y2)

        ax.fill_between(x, y2, 0, alpha=0.3)
        ax.set_xlim([0, 100])
        ax.set_ylim(0)
        ax.set_xlabel('Grade')
        # ax.set_yticklabels([])
        ax.set_title('Prediction of the distribution of the grades')

        filePath = pathlib.Path(__file__).parents[2] / 'media' / f'{ctx.author.name}graph.png'
        plt.savefig(filePath, dpi=72, bbox_inches='tight')
        await ctx.send(file=discord.File(filePath))
        filePath.unlink()

def setup(bot):
    bot.add_cog(MatPlotLib(bot))