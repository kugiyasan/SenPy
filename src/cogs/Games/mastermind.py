import discord
from discord.ext import commands

from ..mofupoints import giveMofuPoints
from ..utils.deleteMessage import deleteMessage

import asyncio
import random
import re
from typing import Optional, List, Tuple


class Mastermind(commands.Cog, name="Games"):
    def __init__(self, bot):
        self.bot = bot
        self.playingUsers = set()

    @commands.command()
    async def stopmm(self, ctx: commands.Context):
        """
        Debug command, call this if mastermind has crashed
        and it thinks that you still have a on going game
        """
        self.playingUsers.discard(ctx.author)
        await ctx.send("You should now be able to start a new game!")

    def generateAnswer(self, guessLength, repeatedColor) -> Optional[List[int]]:
        if repeatedColor:
            answer = [random.randint(1, 6) for _ in range(guessLength)]
        else:
            if guessLength > 6:
                return None

            answer = list(range(1, 7))
            random.shuffle(answer)
            answer = answer[:guessLength]

        return answer

    def judgement(self, guess, answer) -> str:
        guess = [int(i) for i in guess]
        white, brown = 0, 0

        for i in range(1, 7):
            brown += min(guess.count(i), answer.count(i))

        for i in range(len(answer)):
            if answer[i] == guess[i]:
                white += 1

        return "⚪" * white + "🟤" * (brown - white)

    def toEmoji(self, string):
        if type(string) == list:
            string = "".join(str(i) for i in string)

        return (
            string.replace("1", "🔴")
            .replace("2", "🟠")
            .replace("3", "🟡")
            .replace("4", "🟢")
            .replace("5", "🔵")
            .replace("6", "🟣")
        )

    async def winMessage(self, ctx: commands.Context, guessLength: int):
        await ctx.send("Congratulations! You won!")
        await ctx.send(f"{guessLength**2} points will be added to your account!")
        self.playingUsers.discard(ctx.author)
        giveMofuPoints(ctx.author, guessLength ** 2)

    async def getUserInput(
        self, ctx: commands.Context, answer: List[int]
    ) -> Optional[Tuple[discord.Message, str]]:
        def checkresponse(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            m = await self.bot.wait_for("message", timeout=300.0, check=checkresponse)
        except asyncio.TimeoutError:
            await ctx.send(
                "Stopping mastermind, timeout expired\n"
                f"The answer was {self.toEmoji(answer)}"
            )
            self.playingUsers.discard(ctx.author)
            return None

        msg = m.content.replace(" ", "")
        if "stop" in msg.lower():
            await ctx.send(
                f"Stopping the game... The answer was {self.toEmoji(answer)}"
            )
            self.playingUsers.discard(ctx.author)
            return None

        return m, msg

    async def isInvalidMessage(self, ctx, msg, boardMessage, guessLength) -> bool:
        if re.search("show|drop", msg.lower()):
            boardMessage = await ctx.send(boardMessage.content)
            return True

        if re.search("[^1-6]", msg):
            return True
        if len(msg) != guessLength:
            await ctx.send("Please enter a valid guess!", delete_after=10.0)
            return True

        return False

    @commands.command(aliases=["mm"])
    async def mastermind(
        self, ctx: commands.Context, guessLength: int = 6, repeatedColor: bool = True
    ):
        """Play a game of mastermind!"""
        # INIT
        NUMBER_OF_TRIES = 10
        guessLength = max(4, min(10, guessLength))

        answer = self.generateAnswer(guessLength, repeatedColor)
        if not answer:
            await ctx.send("The length of the guess has to be 6 or less!")
            return

        if ctx.author in self.playingUsers:
            await ctx.send("You've already started a game, please stop it first!")
            return
        self.playingUsers.add(ctx.author)

        await ctx.send(
            "1 :🔴\t2 : 🟠\t3 : 🟡\t4 : 🟢\t5 : 🔵\t6 : 🟣\n"
            f"Make your first guess! ({guessLength} digits) "
            '(Type "stop" to stop the game)'
        )

        emptyLine = "⚫" * guessLength + "\t|"
        boardMessage = await ctx.send((emptyLine + "\n") * NUMBER_OF_TRIES)

        # MAIN LOOP
        tryCount = 0
        while tryCount < NUMBER_OF_TRIES:
            userInput = await self.getUserInput(ctx, answer)
            if not userInput:
                return
            m, msg = userInput

            if await self.isInvalidMessage(ctx, msg, boardMessage, guessLength):
                continue

            await deleteMessage(m)

            judge = self.judgement(msg, answer)
            msg = self.toEmoji(msg)

            board = boardMessage.content.replace(emptyLine, msg + "\t|\t" + judge, 1)
            await boardMessage.edit(content=board)

            if judge == "⚪" * guessLength:
                await self.winMessage(ctx, guessLength)
                return

            tryCount += 1

        await ctx.send("You lose! The answer was " + self.toEmoji(answer))
        self.playingUsers.discard(ctx.author)


def setup(bot: commands.Bot):
    bot.add_cog(Mastermind(bot))
