import discord
from discord.ext import commands

import asyncio
import chess


class ChessCog(commands.Cog, name="Games"):
    def __init__(self, bot):
        self.bot = bot
        self.playingUsers = set()
        self.symbolToEmoji = {
            "b": "<:BB:764573853136715827>",
            "k": "<:BK:764573853132259349>",
            "n": "<:BN:764573853132390400>",
            "q": "<:BQ:764573853225451590>",
            "p": "<:BP:764573853119807489>",
            "r": "<:BR:764573853208018964>",
            "B": "<:WB:764573853157949440>",
            "K": "<:WK:764573853233709116>",
            "N": "<:WN:764573853275127840>",
            "P": "<:WP:764573853225582602>",
            "Q": "<:WQ:764573853313400832>",
            "R": "<:WR:764573853259005952>",
        }

    @commands.command()
    async def chess(self, ctx, adversary: discord.Member):
        """Play chess with someone"""
        if adversary.bot:
            await ctx.send("You can't play versus a bot, at least for now")
            return

        if ctx.author in self.playingUsers or adversary in self.playingUsers:
            await ctx.send("You've already started a game, please stop it first!")
            return
        self.playingUsers.update((ctx.author, adversary))

        await ctx.send(
            "CHESS!!\n"
            'The invited person plays first, a valid move is in the form "e2e4" '
            "where e2 is the piece initial coordinate and e4 is the destination\n"
            "If you don't know how to play chess, "
            "go check out the wiki page <https://en.wikipedia.org/wiki/Chess>"
        )

        turn = 0
        board = chess.Board()
        boardMsg = await ctx.send(self.discordBoard(board))

        def checkresponse(m):
            if turn == 1:
                return m.author == ctx.author and m.channel == ctx.channel
            return m.author == adversary and m.channel == ctx.channel

        # MAIN LOOP
        while 1:  # NOT CHECKMATE
            try:
                m = await self.bot.wait_for(
                    "message", timeout=60.0, check=checkresponse
                )
            except asyncio.TimeoutError:
                await ctx.send("Stopping chess, timeout expired")
                await self.endGame(ctx, adversary, turn)
                return

            if m.content.lower() == "stop":
                await self.endGame(ctx, adversary, turn)
                return

            msg = m.content

            try:
                board.push_uci(msg)
            except ValueError as errorMsg:
                await ctx.send(str(errorMsg), delete_after=10.0)
                continue

            boardState = "You're in check!" if board.is_check() else ""

            await boardMsg.delete()
            player = (ctx.author, adversary)[turn]
            boardMsg = await ctx.send(
                self.discordBoard(board) + f"\nit's {player.name}'s turn!\n{boardState}"
            )

            if board.is_checkmate():
                await ctx.send("CHECKMATE!")
                await self.endGame(ctx, adversary, turn)
                return

            turn = (turn + 1) % 2

    async def endGame(self, ctx, adversary, winnerTurn):
        winner = (ctx.author.name, adversary)[winnerTurn]
        await ctx.send(f"\n{winner} wins!")
        self.playingUsers -= {ctx.author, adversary}

    def discordBoard(self, board):
        builder = []

        for y in range(8):
            builder.append([])
            for x in range(8):
                piece = board.piece_at(8 * y + x)

                if piece:
                    builder[y].append(self.symbolToEmoji[piece.symbol()])
                else:
                    builder[y].append(("⬛", "⬜")[(x + y) % 2])

        number = (
            ":one:",
            ":two:",
            ":three:",
            ":four:",
            ":five:",
            ":six:",
            ":seven:",
            ":eight:",
        )
        header = (
            "⬛:regional_indicator_a:"
            ":regional_indicator_b:"
            ":regional_indicator_c:"
            ":regional_indicator_d:"
            ":regional_indicator_e:"
            ":regional_indicator_f:"
            ":regional_indicator_g:"
            ":regional_indicator_h:\n"
        )
        return header + "\n".join(
            number[i] + "".join(row) for i, row in enumerate(builder)
        )


def setup(bot: commands.Bot):
    bot.add_cog(ChessCog(bot))
