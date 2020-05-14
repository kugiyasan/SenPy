import discord
from discord.ext import commands

from cogs.mofupoints import giveMofuPoints
from cogs.utils.deleteMessage import deleteMessage

import asyncio
import logging
import random
import re

class Mastermind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playingUsers = set()

    @commands.command(hidden=True)
    async def gamers(self, ctx):
        if not self.playingUsers:
            await ctx.send('Nobody is playing mastermind')
            return
            
        await ctx.send('Here are the players currently playing mastermind: ' + ', '.join(self.playingUsers))

    def judgement(self, guess, answer):
        guess = [int(i) for i in guess]
        white, brown = 0, 0

        for i in range(1, 7):
            brown += min(guess.count(i), answer.count(i))

        for i in range(len(answer)):
            if answer[i] == guess[i]:
                white += 1

        return '⚪'*white + '🟤'*(brown-white)

    def toEmoji(self, string):
        if type(string) == list:
            string = ''.join(str(i) for i in string)

        return (string.replace('1', '🔴')
                    .replace('2', '🟠')
                    .replace('3', '🟡')
                    .replace('4', '🟢')
                    .replace('5', '🔵')
                    .replace('6', '🟣'))

    @commands.command(aliases=['mm'])
    @commands.bot_has_permissions(manage_messages=True)
    async def mastermind(self, ctx: commands.Context, guessLength: int=6, repeatedColor: bool=True):
        '''Play a game of mastermind!'''

        if ctx.author in self.playingUsers:
            await ctx.send("You've already started a game, please stop it first!")
            return
        self.playingUsers.add(ctx.author)

        # INIT
        NUMBER_OF_TRIES = 10

        if repeatedColor:
            answer = [random.randint(1, 6) for _ in range(guessLength)]
        else:
            if guessLength > 6:
                await ctx.send("The length of the guess has to be 6 or less!")
                return

            answer = list(range(1, 7))
            random.shuffle(answer)
            answer = answer[:guessLength]
        
        logging.info(answer)

        await ctx.send('1 :🔴\t2 : 🟠\t3 : 🟡\t4 : 🟢\t5 : 🔵\t6 : 🟣')
        await ctx.send(f'Make your first guess! ({guessLength} digits) (Type stop to stop the game)')
        
        emptyLine = '⚫'*guessLength + '\t|'
        await ctx.send((emptyLine + '\n') * NUMBER_OF_TRIES)

        def checkresponse(m):
            return (m.author == ctx.author
                and m.channel == ctx.channel)

        # MAIN LOOP
        tryCount = 0
        while tryCount < NUMBER_OF_TRIES:
            try:
                m = await self.bot.wait_for('message',
                                            timeout=1200.0,
                                            check=checkresponse)
            except asyncio.TimeoutError:
                await ctx.send('Stopping mastermind, timeout expired')
                await ctx.send(f'The answer was {self.toEmoji(answer)}')
                self.playingUsers.discard(ctx.author)
                return

            msg = m.content.replace(' ', '')
            if 'stop' in msg.lower():
                await ctx.send('Stopping the game...', delete_after=10.0)
                await ctx.send(f'The answer was {self.toEmoji(answer)}')
                self.playingUsers.discard(ctx.author)
                return
            
            if len(msg) != guessLength or re.search('[^1-6]', msg):
                await ctx.send('Please enter a valid guess!', delete_after=10.0)
                continue
            
            await deleteMessage(m)
            
            judge = self.judgement(msg, answer)
            msg = self.toEmoji(msg)

            async for message in ctx.history():
                if message.author == self.bot.user:
                    if message.content[-1] != '|':
                        continue

                    board = message.content.replace(emptyLine, msg+'\t|\t'+judge, 1)
                    await message.edit(content=board)

                    if judge == '⚪'*guessLength:
                        await ctx.send('Congratulations! You won!')
                        await ctx.send(f'{guessLength**2} points will be added to your account!')
                        self.playingUsers.discard(ctx.author)
                        await giveMofuPoints(ctx.author, guessLength**2)
                        return

                    tryCount += 1
                    break

        await ctx.send('You lose! The answer was ' + self.toEmoji(answer))
        self.playingUsers.discard(ctx.author)

def setup(bot):
    bot.add_cog(Mastermind(bot))