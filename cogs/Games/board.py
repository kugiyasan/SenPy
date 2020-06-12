import numpy as np
import re

from .pieces import *

class Board():
    def __init__(self, onlyPawn=False):
        self.turn = 0
        self.board = np.full((8, 8), None, dtype=object)

        self.board[1] = [Pawn('B') for i in range(8)]
        self.board[6] = [Pawn('W') for i in range(8)]

        if onlyPawn:
            self.board[0][3] = King('B')
            self.board[7][3] = King('W')
            return

        self.board[0] = [
            Rook('B'),
            Knight('B'),
            Bishop('B'),
            King('B'),
            Queen('B'),
            Bishop('B'),
            Knight('B'),
            Rook('B')
        ]
        self.board[7] = [
            Rook('W'),
            Knight('W'),
            Bishop('W'),
            King('W'),
            Queen('W'),
            Bishop('W'),
            Knight('W'),
            Rook('W')
        ]

    def movePiece(self, initSq, destSq):
        '''The Board object will make general check to see if the move is valid,
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
            print(emptySquaresCoords)
            for coord in emptySquaresCoords:
                if self.board[coord] != None:
                    raise GameError('There is a piece in the way!')
            
            # pawn promotion, default to Queen
            #? maybe offer to promote to Knight
            print(destSq[0])
            if destSq[0] == 0 or destSq[0] == 7:
                print('here')
                self.board[initSq] = Queen(self.board[initSq].COLOR)
        
        elif type(self.board[initSq]) == Pawn:
            # exception: pawn moving in diagonal need a Piece to kill at destSq
            if self.board[destSq] == None:
                # double exception: en passant capture
                EnPassantPawn = self.board[initSq[0], destSq[1]]
                if type(EnPassantPawn) == Pawn and EnPassantPawn.doubleStartTurn+1 == self.turn:
                    self.board[initSq[0], destSq[1]] = None
                    
                else:
                    raise GameError("Pawn moving in diagonal doesn't have a Piece to kill at destSq")

        self.board[destSq] = self.board[initSq]
        self.board[initSq] = None

    def __repr__(self):
        board = np.copy(self.board)

        for x in range(8):
            for y in range(8):
                if board[x][y] == None:
                    board[x][y] = ('⬛', '⬜')[(x + y) % 2]
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
    mode = input('only pawn? (default no): ').lower()
    yesWords = {'y', 'yes', 'true', '1'}
    if mode in yesWords:
        game = Board(onlyPawn=True)
    else:
        game = Board()

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
