import discord
from discord.ext import commands

from cogs.Games.board import Board, GameError
import asyncio


class ChessCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playingUsers = set()

    @commands.command(hidden=True)
    async def nerds(self, ctx):
        if not self.playingUsers:
            await ctx.send('Nobody is playing chess')
            return
            
        players = ', '.join(p.name for p in self.playingUsers)
        await ctx.send('Here is/are the player(s) currently playing chess: ' + players)

    @commands.command()
    async def chess(self, ctx, adversary: discord.Member):
        """Play a chess game with someone"""
        if adversary.bot:
            await ctx.send("You can't play versus a bot, at least for now")
            return

        if ctx.author in self.playingUsers or adversary in self.playingUsers:
            await ctx.send("You've already started a game, please stop it first!")
            return
        self.playingUsers.update((ctx.author, adversary))
        
        turn = 0
        game = Board()
        board = await ctx.send(str(game))

        def checkresponse(m):
            if turn == 1:
                return (m.author == ctx.author
                    and m.channel == ctx.channel)
            return (m.author == adversary
                and m.channel == ctx.channel)
        
        # MAIN LOOP
        while 1: # NOT CHECKMATE
            try:
                m = await self.bot.wait_for(
                    'message',
                    timeout=60.0,
                    check=checkresponse
                )
            except asyncio.TimeoutError:
                await ctx.send('Stopping chess, timeout expired')
                await self.endGame(ctx, adversary, (turn, str(game)))
                return

            if m.content.lower() == 'stop':
                await self.endGame(ctx, adversary, (turn, str(game)))

            msg = m.content.split()
            if len(msg) != 2:
                await ctx.send('Too many arguments were given', delete_after=10.0)
                continue

            try:
                gameState = game.movePiece(*msg)
            except GameError as error:
                await ctx.send(str(error), delete_after=10.0)
                continue
            
            if gameState:
                await self.endGame(ctx, adversary, gameState)
                return

            await board.delete()
            board = await ctx.send(str(game))
            turn = (turn + 1) % 2
        
    async def endGame(self, ctx, adversary, gameState):
        winner = (ctx.author.name, adversary)[gameState[0]]
        await ctx.send(gameState[1] + f'\n{winner} wins!')
        self.playingUsers -= {ctx.author, adversary}

def setup(bot):
    bot.add_cog(ChessCog(bot))