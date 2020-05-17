import discord
from discord.ext import commands

import torch
import torch.nn as nn
import torch.nn.functional as F

import io
import numpy as np
import matplotlib.pyplot as plt
import pathlib
import re
from PIL import Image

class BasicCNN(nn.Module):
    def __init__(self):
        super().__init__()
        # 1 input image channel, 6 output channels, 3x3 square convolution
        # kernel
        self.conv1 = nn.Conv2d(1, 6, 3)
        self.conv2 = nn.Conv2d(6, 16, 3)
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(400, 120)  # 16* 6*6 from image dimension
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # Max pooling over a (2, 2) window
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        # If the size is a square you can only specify a single number
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
        
    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features

class NN(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.device = torch.device("cpu")

        self.model = BasicCNN().to(self.device)
        self.model.load_state_dict(torch.load("tests/data/MNISTdigitreader2.pt"))
        self.model.eval()

    @commands.command(aliases=['digits'])
    async def digit(self, ctx: commands.Context):
        """Guess the digit in the image"""
        images = ctx.message.attachments
        if (len(images) == 0
            or not re.search(r'(\.png)|(\.jpg)|(\.jpeg)', images[0].filename.lower())):
            await ctx.send('Please attach an png or jpg image with your message!')
            return

        PATH = f"media/digit_{ctx.author.name}.png"
        await images[0].save(PATH)

        im = Image.open(PATH).convert("L").resize((28, 28))

        pix = np.array(im.getdata()).reshape(im.size[0], im.size[1])
        pix = pix.astype('float32')
        pix /= 255.0
        pix.shape = (1, 1, 28, 28)

        plt.subplots()
        plt.axis('off')
        heatmap = plt.imshow(pix[0, 0])
        plt.colorbar(heatmap)

        filePath = pathlib.Path(__file__).parents[1] / 'media' / f'{ctx.author.name}graph.png'
        plt.savefig(filePath, dpi=72, bbox_inches='tight')
        plt.close('all')

        await ctx.send(file=discord.File(filePath))
        filePath.unlink()

        inp = torch.from_numpy(pix).to(self.device)
        result = self.model(inp)
        await ctx.send(f"I'm guessing that the number in the picture is a {result.argmax()}!")

def setup(bot):
    bot.add_cog(NN(bot))