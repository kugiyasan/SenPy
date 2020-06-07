from abc import ABC, abstractmethod
import numpy as np
import re

class GameError(Exception):
    pass

class Piece(ABC):
    def __init__(self, color):
        if color != 'W' and color != 'B':
            raise ValueError('color should be equal to "W" or "B"')

        self.COLOR = color

    def __repr__(self):
        return self.COLOR + type(self).__name__[0]

    @abstractmethod
    def checkIfValid(self, initSq, destSq, color):
        if initSq == destSq:
            raise GameError('You need to move the piece')

        if self.COLOR != color:
            # We already checked for empty square in board.py
            raise GameError('Piece of the adversary at initSq')


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hasMoved = False

    def checkIfValid(self, initSq, destSq, color):
        super().checkIfValid(initSq, destSq, color)
        
        dx = destSq[1] - initSq[1]
        dy = destSq[0] - initSq[0]
        side = -1 if self.COLOR == 'W' else 1

        # diagonal attack
        if abs(dx) == 1 and dy == side:
            return

        if dx != 0:
            raise GameError("Pawn can't move horizontally")

        if abs(dy) > 2:
            raise GameError("Pawn can't move more than 2 squares in a straight line")

        if abs(dy) == 2:
            if self.hasMoved:
                raise GameError("Pawn can only move 2 squares at the beginning")
            
            self.hasMoved = True
            return ((initSq[0]+(destSq[0]-initSq[0])//2, initSq[1]), destSq)

        return (destSq,)