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
    def checkIfValid(self, initSq, destSq, turn):
        if initSq == destSq:
            raise GameError('You need to move the piece')

        if ('W', 'B').index(self.COLOR) != turn % 2:
            # We already checked for empty square in board.py
            raise GameError('Piece of the adversary at initSq')

    def move(self):
        pass


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hasMoved = False
        self.doubleStartTurn = 0

    def checkIfValid(self, initSq, destSq, turn):
        super().checkIfValid(initSq, destSq, turn)
        
        dx = destSq[1] - initSq[1]
        dy = destSq[0] - initSq[0]
        side = -1 if self.COLOR == 'W' else 1
        print(side)

        # diagonal attack
        if abs(dx) == 1 and dy == side:
            return

        if dx != 0:
            raise GameError("Pawn can't move horizontally")

        if dy * side == 2:
            if self.hasMoved:
                raise GameError("Pawn can only move 2 squares at the beginning")
            
            self.doubleStartTurn = turn
            return ((initSq[0]+(destSq[0]-initSq[0])//2, initSq[1]), destSq)

        if dy * side == 1:
            return (destSq,)

        raise GameError("Pawn can't move more than 2 squares in a straight line")

    def move(self):
        self.hasMoved = True


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hasMoved = False

    def checkIfValid(self, initSq, destSq, turn):
        super().checkIfValid(initSq, destSq, turn)

        dx = destSq[1] - initSq[1]
        dy = destSq[0] - initSq[0]

        #TODO move the Rook
        # Roque
        # if dy == 0 and not self.hasMoved:
        #     if dx == 2:
        #         return (destSq, (destSq[0], destSq[1]-1))
        #     if dx == -2:
        #         return ((destSq[0], destSq[1]-1), destSq, (destSq[0], destSq[1]+1))

        if abs(dx) < 2 and abs(dy) < 2:
            return
        
        #TODO check if check/checkmate by looking around like every Piece

        raise GameError("You can't normally move the King more than 2 squares")

    def move(self):
        self.hasMoved = True

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)

    def __repr__(self):
        return self.COLOR + 'N'

    def checkIfValid(self, initSq, destSq, turn):
        super().checkIfValid(initSq, destSq, turn)

        dx = abs(destSq[1] - initSq[1])
        dy = abs(destSq[0] - initSq[0])

        if (dx == 1 and dy == 2) or (dx == 2 and dy == 1):
            return

        raise GameError("The Knight moves in L shape")

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hasMoved = False

    def checkIfValid(self, initSq, destSq, turn):
        super().checkIfValid(initSq, destSq, turn)

        dx = destSq[1] - initSq[1]
        dy = destSq[0] - initSq[0]

        if dx == 0:
            a = min(destSq[0], initSq[0]) + 1
            b = max(destSq[0], initSq[0])
            return ((x, initSq[1]) for x in range(a, b))

        elif dy == 0:
            a = min(destSq[1], initSq[1]) + 1
            b = max(destSq[1], initSq[1])
            return ((initSq[0], x) for x in range(a, b))

        raise GameError("The Rook can only move on a horizontal or vertical line")

    def move(self):
        self.hasMoved = True

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)

    def checkIfValid(self, initSq, destSq, turn):
        super().checkIfValid(initSq, destSq, turn)

        dx = destSq[1] - initSq[1]
        dy = destSq[0] - initSq[0]

        if abs(dx) != abs(dy):
            raise GameError("The Bishop can only move on a diagonal line")
        
        minx = initSq[1]
        miny = initSq[0]
        maxx = destSq[1]
        if dx == dy:
            return ((miny+x, minx+x) for x in range(miny+1, maxx))

        elif dx == -dy:
            return ((miny-x, minx+x) for x in range(miny+1, maxx))

class Queen(Bishop):
    def checkIfValid(self, initSq, destSq, turn):
        try:
            return super().checkIfValid(initSq, destSq, turn)
        except:
            pass
        
        dx = destSq[1] - initSq[1]
        dy = destSq[0] - initSq[0]

        if dx == 0:
            a = min(destSq[0], initSq[0]) + 1
            b = max(destSq[0], initSq[0])
            return ((x, initSq[1]) for x in range(a, b))

        elif dy == 0:
            a = min(destSq[1], initSq[1]) + 1
            b = max(destSq[1], initSq[1])
            return ((initSq[0], x) for x in range(a, b))

        raise GameError("The Queen can move on a horizontal, vertical or a diagonal line")