import random
from boardState import BoardState

"""
    -------------
    | 7 | 0 | 1 |
    | 6 | x | 2 |
    | 5 | 4 | 3 |
    -------------
"""

TEACHER = -1
ME = 1

class Player:    
    def __init__(self, str_name = "me"):
        if str_name == "me":
            self.player = 1 # Me
        else:
            self.plyer = -1 # Teacher
        self.preBoard = BoardState()
    
    def __str__(self):
        return self.name

    def move(self, board):
        _boardSate = BoardState(board)
        last_move = self.getlast_move(_boardSate)
        move = _boardSate.listCells_CanMove(self.player, self.preBoard, last_move)
        if len(move) == 0:
            return None
        choose = random.choice(move)
        row, col, dir = choose[0], choose[1], choose[2]
        (newrow, newcol) = _boardSate.updateCell(row, col, dir)
        self.preBoard = BoardState([[0 for j in range(self.n)] for i in range(self.n)], self.n)
        self.preBoard.board = [values[:] for values in _boardSate.board]

        start = (row, col)
        end = (newrow, newcol)
        self.preBoard = self.preBoard.change(start, end)
        return (start, end)

    def getlast_move(self, boardState : "BoardState"):
        for row in range(self.preBoard.n):
            for col in range(self.preBoard.n):
                if self.preBoard[row][col] != 0 and boardState[(row, col)] == 0:
                    start = (row, col)
                if self.preBoard[row][col] == 0 and boardState[(row, col)] != 0:
                    end = (row, col)
        return (start, end)

PLAYER = Player("me")

def move(board, player):
    return PLAYER.move(board)