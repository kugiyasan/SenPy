import numpy as np
import re

from .pieces import *

class Board():
    def __init__(self, onlyPawn=False, noPawn=False):
        self.turn = 0
        self.KingsPosition = [(7, 4), (0, 4)]

        self.board = np.full((8, 8), None, dtype=object)

        if not noPawn:
            self.board[1] = [Pawn('B') for i in range(8)]
            self.board[6] = [Pawn('W') for i in range(8)]

        if onlyPawn:
            self.board[self.KingsPosition[1]] = King('B')
            self.board[self.KingsPosition[0]] = King('W')
            return

        self.board[0] = [
            Rook('B'),
            Knight('B'),
            Bishop('B'),
            Queen('B'),
            King('B'),
            Bishop('B'),
            Knight('B'),
            Rook('B')
        ]
        self.board[7] = [
            Rook('W'),
            Knight('W'),
            Bishop('W'),
            Queen('W'),
            King('W'),
            Bishop('W'),
            Knight('W'),
            Rook('W')
        ]

    def movePiece(self, initSq, destSq):
        '''The Board object will make general check to see if the move is possible,
            then it is going to ask the Piece object if it is a legal move
            and ask at the same time for squares that needs to be empty in order
            to ensure the coplete legality of the move'''

        initSq = initSq.lower()
        destSq = destSq.lower()

        if (not re.match('[a-h][1-8]$', initSq)
            or not re.match('[a-h][1-8]$', destSq)):
            raise GameError('Bad coordinates')
        
        initSq = (8-int(initSq[1]), ord(initSq[0])-ord('a'))
        destSq = (8-int(destSq[1]), ord(destSq[0])-ord('a'))

        if not self.board[initSq]:
            raise GameError('No piece at initSq')

        if str(self.board[destSq])[0] == str(self.board[initSq])[0]:
            # wrong initSq color and wrong destSq won't be catched here
            raise GameError('initSq and destSq have Pieces of the same color')

        self._move(initSq, destSq)

        self.turn += 1

    def _move(self, initSq, destSq):
        emptySquaresCoords = self.board[initSq].checkIfValid(initSq, destSq, self.turn)
        self.board[initSq].move()

        if emptySquaresCoords:
            for coord in emptySquaresCoords:
                if self.board[coord] != None:
                    raise GameError('There is a piece in the way!')
            
            # Pawn promotion, default to Queen
            #? Maybe offer to promote to Knight
            if (type(self.board[initSq]) == Pawn
                and (destSq[0] == 0 or destSq[0] == 7)):
                self.board[initSq] = Queen(self.board[initSq].COLOR)

            # Castling
            elif type(self.board[initSq]) == King:
                if (destSq[1] - initSq[1] == 2
                    and type(self.board[initSq[0], 7]) == Rook
                    and not self.board[initSq[0], 7].hasMoved):
                    self._move((initSq[0], 7), (initSq[0], 4))

                elif (destSq[1] - initSq[1] == -2
                    and type(self.board[initSq[0], 0]) == Rook
                    and not self.board[initSq[0], 0].hasMoved):
                    self._move((initSq[0], 0), (initSq[0], 2))
                
                else:
                    raise GameError("You can't do the castling!")
        
        elif type(self.board[initSq]) == Pawn:
            # exception: pawn moving in diagonal need a Piece to kill at destSq
            if self.board[destSq] == None:
                # double exception: en passant capture
                EnPassantPawn = self.board[initSq[0], destSq[1]]
                if type(EnPassantPawn) == Pawn and EnPassantPawn.doubleStartTurn+1 == self.turn:
                    self.board[initSq[0], destSq[1]] = None
                    
                else:
                    raise GameError("Pawn moving in diagonal doesn't have a Piece to kill at destSq")

        elif type(self.board[initSq]) == King:
            if self.board[initSq].COLOR == 'W':
                self.KingsPosition[0] = destSq
            else:
                self.KingsPosition[0] = destSq

        temp = self.board[initSq]
        self.board[initSq] = None

        if self.kingIsInCheck(self.KingsPosition[self.turn % 2]):
            self.board[initSq] = temp
            raise GameError("You're King is in check!")

        self.board[destSq] = temp

        if self.kingIsInCheck(self.KingsPosition[(self.turn+1) % 2]):
            print('Check!')

    def kingIsInCheck(self, position):
        y, x = position
        side = 1 if self.turn % 2 else -1

        # Check made by Pawn or Knight
        PawnChecks = ((y+side, x+1), (y+side, x-1))
        KnightChecks = ((y+1, x+2), (y+1, x-2), (y-1, x+2), (y-1, x-2),
                        (y+2, x+1), (y+2, x-1), (y-2, x+1), (y-2, x-1))  

        return any((
            self.checkSquares(PawnChecks, position, Pawn),
            self.checkSquares(KnightChecks, position, Knight),
            # Right, Left, Down, Up, UpLeft, DownRight, UpRight, DownLeft
            self.lookLine(x, y, (Rook, Queen), 8-x,  0,  1),
            self.lookLine(x, y, (Rook, Queen), x+1,  0, -1),
            self.lookLine(x, y, (Rook, Queen), 8-y,  1,  0),
            self.lookLine(x, y, (Rook, Queen), y+1, -1,  0),
            self.lookLine(x, y, (Bishop, Queen), min(x, y)+1,   -1, -1),
            self.lookLine(x, y, (Bishop, Queen), 8-max(x, y),    1,  1),
            self.lookLine(x, y, (Bishop, Queen), min(7-x, y)+1, -1,  1),
            self.lookLine(x, y, (Bishop, Queen), min(7-y, x)+1,  1, -1)
        ))

    def checkSquares(self, squares, kingPosition, pieceType):
        for square in squares:
            if square[0] < 0 or square[0] > 7 or square[1] < 0 or square[1] > 7:
                continue
            if (type(self.board[square]) == pieceType
                and self.board[square].COLOR != self.board[kingPosition].COLOR):
                return True

    def lookLine(self, x, y, pieces, rangeEnd, ysign, xsign):
        for i in range(1, rangeEnd):
            if (type(self.board[y+ysign*i, x+xsign*i]) in pieces
                and self.board[y+ysign*i, x+xsign*i].COLOR != self.board[y, x].COLOR):
                return True
            elif self.board[y+ysign*i, x+xsign*i] != None:
                break

    def __repr__(self):
        board = np.copy(self.board)

        for x in range(8):
            for y in range(8):
                if board[x][y] == None:
                    board[x][y] = ('⬜', '⬛')[(x + y) % 2]
                    continue
                
                board[x, y] = str(board[x, y])

                board[x][y] = (board[x][y]
                    .replace('BB', '<:BB:717894296396890154>')
                    .replace('BK', '<:BK:717894296459542587>')
                    .replace('BN', '<:BN:717894296329781250>')
                    .replace('BP', '<:BP:717894296572788787>')
                    .replace('BQ', '<:BQ:717894296409473047>')
                    .replace('BR', '<:BR:717894296870584320>')
                    .replace('WB', '<:WB:717894297109659748>')
                    .replace('WK', '<:WK:717894296673452041>')
                    .replace('WN', '<:WN:717894296698617877>')
                    .replace('WP', '<:WP:717894296992219176>')
                    .replace('WQ', '<:WQ:717894296967315517>')
                    .replace('WR', '<:WR:717894296807931984>'))

        number = (':eight:', ':seven:', ':six:', ':five:',
                  ':four:', ':three:', ':two:', ':one:')
        header = ('⬛:regional_indicator_a:'
                + ':regional_indicator_b:'
                + ':regional_indicator_c:'
                + ':regional_indicator_d:'
                + ':regional_indicator_e:'
                + ':regional_indicator_f:'
                + ':regional_indicator_g:'
                + ':regional_indicator_h:\n')
        return header + '\n'.join(number[i]+''.join(row) for i, row in enumerate(board))
    
    @property
    def terminalBoard(self):
        board = np.copy(self.board)

        for x in range(8):
            for y in range(8):
                if board[x][y] == None:
                    board[x][y] = ('⬛', '⬜')[(x + y) % 2]
                    continue
                
                board[x, y] = str(board[x, y])
        return '\n'.join(''.join(row) for row in board)
        

if __name__ == "__main__":
    onlyPawn = input('only pawn? (default no): ').lower()
    noPawn = input('no pawn? (default no): ').lower()
    yesWords = {'y', 'yes', 'true', '1'}

    if onlyPawn in yesWords:
        onlyPawn = True
    else:
        onlyPawn = False

    if noPawn in yesWords:
        noPawn = True
    else:
        noPawn = False

    game = Board(onlyPawn=onlyPawn, noPawn=noPawn)

    while 1:
        print(game.terminalBoard)

        try:
            initSq, destSq = input('Coordinates: ').split()
        except ValueError:
            print('Enter valid coordinates')
            continue

        try:
            game.movePiece(initSq, destSq)
        except GameError as errorMessage:
            print(errorMessage)

        # status, statusMsg = game.movePiece(initSq, destSq)
        # if statusMsg == 'ok':
        #     pass
        # elif statusMsg == 'error':
        #     print(statusMsg)
        # elif statusMsg == 'info':
        #     print(statusMsg)
