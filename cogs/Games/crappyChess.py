import numpy as np
import re

class ChessGame():
    def __init__(self):
        self.BOARDSIZE = 8
        self.turn = 0

        self.BKmoved = False
        self.LBRmoved = False
        self.RBRmoved = False
        self.WKmoved = False
        self.LWRmoved = False
        self.RWRmoved = False

        # init board and initial pawn places
        self.board = np.full((self.BOARDSIZE, self.BOARDSIZE), '00', dtype='|S2')
        self.board[0] = ['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR']
        self.board[7] = ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR']
        self.board[1] = ['BP'] * self.BOARDSIZE
        self.board[6] = ['WP'] * self.BOARDSIZE

    def playerMove(self, color, initSq, destSq, pawnPromotion='Q', doNotUpdateTurn=False):
        if self.turn != color:
            raise GameError("Not this player's turn")

        initSq = initSq.lower()
        destSq = destSq.lower()

        if (not re.match('[a-h][1-8]$', initSq)
            or not re.match('[a-h][1-8]$', destSq)):
            raise GameError('Bad coordinates')
        
        initSq = (self.BOARDSIZE-int(initSq[1]), ord(initSq[0])-ord('a'))
        destSq = (self.BOARDSIZE-int(destSq[1]), ord(destSq[0])-ord('a'))

        if initSq == destSq:
            raise GameError('You need to move the pawn')
        
        if not chr(self.board[initSq][0]) == ('W', 'B')[self.turn]:
            raise GameError('No pawn or pawn of the adversary at initSq')

        if chr(self.board[destSq][0]) == ('W', 'B')[self.turn]:
            raise GameError('There is already one of your pawn at destSq')

        if self.fordiddenMoves(self.board[initSq], initSq, destSq):
            raise GameError('Illegal move for this pawn')

        if initSq == (0, 0):
            self.LBRmoved = True
        elif initSq == (7, 0):
            self.LWRmoved = True
        elif initSq == (0, 7):
            self.RBRmoved = True
        elif initSq == (7, 7):
            self.RWRmoved = True
        elif initSq == (0, 4):
            self.BKmoved = True
        elif initSq == (7, 4):
            self.WKmoved = True

        if self.board[destSq][1] == b'K':
            winner = ('White', 'Black')[self.turn]
            print(f'{winner} won!')
            return self.turn, self.emojiBoard

        self.board[destSq] = self.board[initSq]
        self.board[initSq] = '00'

        if self.board[destSq][1] == b'P' and (destSq[0] == 0 or destSq[0] == 7):
            print('Pawn promotion!')
            self.board[destSq][1] = pawnPromotion.encode()

        if not doNotUpdateTurn:
            self.turn = (self.turn + 1) % 2

    def pawnLogic(self, dx, dy, pawn, initSq, destSq, side):
        if dx == 1 and dy == side and self.board[destSq] != b'00':
            return False
        elif dx != 0 or self.board[destSq] != b'00':
            return True
        elif (dy == side*2 and initSq[0] == int(-2.5*side + 3.5)
            and self.board[initSq[0]+side, initSq[1]] == b'00'):
            return False
        elif dy == side:
            return False
        return True
    
    def collisionDetection(self, initSq, destSq):
        dy = destSq[0]-initSq[0]
        dx = destSq[1]-initSq[1]

        if dx == 0:
            moveLine = self.board[min(destSq[0], initSq[0])+1:max(destSq[0],initSq[0]), initSq[1]]

        elif dy == 0:
            moveLine = self.board[initSq[0], min(destSq[1], initSq[1])+1:max(destSq[1],initSq[1])]

        elif dx == dy:
            moveLine = np.diag(np.fliplr(self.board), k=3-initSq[1]-initSq[0])

        elif dx == -dy:
            moveLine = np.diag(self.board, k=initSq[1]-initSq[0])
        
        else:
            raise GameError('Collision detection failed')

        print(moveLine)
        if len(set(moveLine)) != 1:
            return True

        return False

    def fordiddenMoves(self, pawn, initSq, destSq):
        dy = destSq[0]-initSq[0]
        dx = destSq[1]-initSq[1]
        print(pawn, dx, dy)

        if pawn == b'WP':
            return self.pawnLogic(abs(dx), dy, pawn, initSq, destSq, -1)
            
        elif pawn == b'BP':
            return self.pawnLogic(abs(dx), dy, pawn, initSq, destSq, 1)
        
        pawnType = chr(pawn[1])

        if pawnType == 'N':
            if not((abs(dx)==1 and abs(dy)==2) or (abs(dx)==2 and abs(dy)==1)):
                return True
        elif pawnType == 'K':
            if dy == 0:
                if (dx == 2 
                    and not self.WKmoved
                    and pawn == b'WK'
                    and not self.RWRmoved):
                        self.playerMove(0, 'h1', 'f1', doNotUpdateTurn=True)
                elif (dx == -2 
                    and not self.WKmoved
                    and pawn == b'WK'
                    and not self.LWRmoved):
                        self.playerMove(0, 'a1', 'd1', doNotUpdateTurn=True)
                elif (dx == 2 
                    and not self.BKmoved
                    and pawn == b'WK'
                    and not self.RWRmoved):
                        self.playerMove(1, 'h8', 'f8', doNotUpdateTurn=True)
                elif (dx == -2 
                    and not self.WKmoved
                    and pawn == b'WK'
                    and not self.LWRmoved):
                        self.playerMove(1, 'a8', 'd8', doNotUpdateTurn=True)

            elif not(abs(dx) < 2 and abs(dy) < 2):
                return True

        # collision detection
        elif pawnType == 'R':
            if (abs(dx) != 0 and abs(dy) != 0
                or self.collisionDetection(initSq, destSq)):
                return True
        elif pawnType == 'B':
            if (abs(dx) != abs(dy)
                or self.collisionDetection(initSq, destSq)):
                return True
        elif pawnType == 'Q':
            if (np.arctan(abs(dy)/abs(dx)) % (np.pi/4) != 0.0
                or self.collisionDetection(initSq, destSq)):
                return True
        
        else:
            raise GameError('Unknown pawn')

        return False

    @property
    def emojiBoard(self):
        board = self.board.tolist()

        for x in range(self.BOARDSIZE):
            for y in range(self.BOARDSIZE):
                if board[x][y] == b'00':
                    board[x][y] = ('⬛', '⬜')[(x + y) % 2]
                    continue
                
                board[x][y] = board[x][y].decode("utf-8")

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

        number = (':eight:', ':seven:', ':six:', ':five:', ':four:', ':three:', ':two:', ':one:')
        header = '⬛:regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d::regional_indicator_e::regional_indicator_f::regional_indicator_g::regional_indicator_h:\n'
        return header + '\n'.join(number[i]+''.join(row) for i, row in enumerate(board))

    def __repr__(self):
        return self.emojiBoard

    def movePiece(self, *args):
        return self.playerMove(self.turn, *args)

class GameError(Exception):
    pass

if __name__ == "__main__":
    game = ChessGame()
    print(game.emojiBoard)
    
    while 1:
        print('White turn!')
        game.playerMove(0, input('initSq: '), input('destSq: '))
        print(game.emojiBoard)

        print('Black turn!')
        game.playerMove(1, input('initSq: '), input('destSq: '))
        print(game.emojiBoard)
    