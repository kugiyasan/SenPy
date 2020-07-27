import discord
from discord.ext import commands

from cogs.mofupoints import giveMofuPoints
from cogs.utils.deleteMessage import deleteMessage

import asyncio
import random
import re

playingUsers = set()

class Mastermind(commands.Cog, name="Games"):
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
    async def mastermind(self, ctx: commands.Context, guessLength: int=6, repeatedColor: bool=True):
        '''Play a game of mastermind!'''

        # INIT
        NUMBER_OF_TRIES = 10
        if guessLength < 4:
            await ctx.send("Choose a harder difficulty!")
            return
        if guessLength > 10:
            await ctx.send("Choose a easier difficulty!")
            return

        if repeatedColor:
            answer = [random.randint(1, 6) for _ in range(guessLength)]
        else:
            if guessLength > 6:
                await ctx.send("The length of the guess has to be 6 or less!")
                return

            answer = list(range(1, 7))
            random.shuffle(answer)
            answer = answer[:guessLength]

        if ctx.author in playingUsers:
            await ctx.send("You've already started a game, please stop it first!")
            return
        playingUsers.add(ctx.author)

        text = ('1 :🔴\t2 : 🟠\t3 : 🟡\t4 : 🟢\t5 : 🔵\t6 : 🟣\n'
            + f'Make your first guess! ({guessLength} digits) (Type "stop" to stop the game)')
        await ctx.send(text)
        
        emptyLine = u'⚫'*guessLength + '\t|'
        boardMessage = await ctx.send((emptyLine + '\n') * NUMBER_OF_TRIES)

        def checkresponse(m):
            return (m.author == ctx.author
                and m.channel == ctx.channel)

        # MAIN LOOP
        tryCount = 0
        while tryCount < NUMBER_OF_TRIES:
            try:
                m = await self.bot.wait_for('message',
                                            timeout=300.0,
                                            check=checkresponse)
            except asyncio.TimeoutError:
                await ctx.send('Stopping mastermind, timeout expired')
                await ctx.send(f'The answer was {self.toEmoji(answer)}')
                playingUsers.discard(ctx.author)
                return

            msg = m.content.replace(' ', '')
            if 'stop' in msg.lower():
                await ctx.send('Stopping the game...', delete_after=10.0)
                await ctx.send(f'The answer was {self.toEmoji(answer)}')
                playingUsers.discard(ctx.author)
                return

            if 'show' in msg.lower() or 'drop' in msg.lower():
                boardMessage = await ctx.send(boardMessage.content)
                continue
            
            if re.search('[^1-6]', msg):
                continue
            if len(msg) != guessLength:
                await ctx.send('Please enter a valid guess!', delete_after=10.0)
                continue

            await deleteMessage(m)
            
            judge = self.judgement(msg, answer)
            msg = self.toEmoji(msg)

            board = boardMessage.content.replace(emptyLine, msg+'\t|\t'+judge, 1)
            await boardMessage.edit(content=board)

            if judge == '⚪'*guessLength:
                await ctx.send('Congratulations! You won!')
                await ctx.send(f'{guessLength**2} points will be added to your account!')
                playingUsers.discard(ctx.author)
                await giveMofuPoints(ctx.author, guessLength**2)
                return

            tryCount += 1

        await ctx.send('You lose! The answer was ' + self.toEmoji(answer))
        playingUsers.discard(ctx.author)

def setup(bot):
    bot.add_cog(Mastermind(bot))