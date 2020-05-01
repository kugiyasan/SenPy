import discord
from discord.ext import commands

import asyncio
import random
import re

class Mastermind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def judgement(self, guess, answer):
        guess = [int(i) for i in guess]
        white, brown = 0, 0

        for i in range(1, 7):
            brown += min(guess.count(i), answer.count(i))

        for i in range(len(answer)):
            if answer[i] == guess[i]:
                white += 1

        return ':white_circle:'*white + ':brown_circle:'*(brown-white)

    def toEmoji(self, string):
        if type(string) == list:
            string = ''.join(str(i) for i in string)

        return (string.replace('1', ':red_circle:')
                    .replace('2', ':orange_circle:')
                    .replace('3', ':yellow_circle:')
                    .replace('4', ':green_circle:')
                    .replace('5', ':blue_circle:')
                    .replace('6', ':purple_circle:'))

    @commands.command(aliases=['mm'])
    async def mastermind(self, ctx: commands.Context, guessLength: int=6):
        '''Play a game of mastermind!'''
        numberOfTries = 10
        
        answer = [random.randint(1, 6) for _ in range(guessLength)]

        await ctx.send('1 : red\t2 : orange\t3 : yellow\t4 : green\t5 : blue\t6 : purple')
        await ctx.send(f'Make your first guess! ({guessLength} digits) (Type stop to stop the game)')
        
        emptyLine = ':black_circle:'*guessLength + '\t|'
        await ctx.send((emptyLine + '\n') * numberOfTries)

        def checkresponse(m):
            return (m.author == ctx.author
                and m.channel == ctx.channel)

        tryCount = 0
        while tryCount < numberOfTries:
            try:
                msg = await self.bot.wait_for('message',
                                            timeout=300.0,
                                            check=checkresponse)
            except asyncio.TimeoutError:
                await ctx.send('Stopping mastermind, timeout expired')
                return

            msg = msg.content.replace(' ', '')
            if msg.lower() == 'stop':
                await ctx.send('Stopping the game...', delete_after=10.0)
                return
            
            if len(msg) != guessLength or re.search('[^1-6]', msg):
                await ctx.send('Please enter a valid guess!', delete_after=10.0)
                continue
            
            judge = self.judgement(msg, answer)
            msg = self.toEmoji(msg)

            async for message in ctx.history():
                if message.author == ctx.author:
                    try:
                        await message.delete()
                    except:
                        pass

                if message.author == self.bot.user:
                    if message.content[0] != ':':
                        continue

                    board = message.content.replace(emptyLine, msg+'\t|\t'+judge, 1)
                    await message.edit(content=board)

                    if judge == ':white_circle:'*guessLength:
                        await ctx.send('Congratulations! You won!')
                        return

                    tryCount += 1
                    break

        await ctx.send('You lose! The answer was ' + self.toEmoji(answer))

def setup(bot):
    bot.add_cog(Mastermind(bot))