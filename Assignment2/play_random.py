import random
from boardState import BoardState

"""
    -------------
    | 7 | 0 | 1 |
    | 6 | x | 2 |
    | 5 | 4 | 3 |
    -------------
"""

TEACHER = 1 # Quan O
ME = -1 # Quan X

class Player_random:    
    def __init__(self, str_name = "me"):
        if str_name == "me":
            self.player = ME # Me
        else:
            self.plyer = TEACHER # Teacher
        self.preBoard = BoardState()
    
    def __str__(self):
        return self.player

    def move(self, board, player):
        _boardSate = BoardState(board)
        last_move = self.getlast_move(_boardSate)
        move = _boardSate.listCells_CanMove(player, self.preBoard, last_move)
        if len(move) == 0:
            return None
        choose = random.choice(move)
        row, col, dir = choose[0], choose[1], choose[2]
        (newrow, newcol) = _boardSate.updateCell(row, col, dir)

        start = (row, col)
        end = (newrow, newcol)
        self.preBoard = _boardSate.change(start, end)
        return (start, end)

    def getlast_move(self, boardState : "BoardState"):
        start = (-1, -1)
        end = (-1, -1)
        for row in range(self.preBoard.n):
            for col in range(self.preBoard.n):
                if self.preBoard.board[row][col] != 0 and boardState.board[row][col] == 0:
                    start = (row, col)
                if self.preBoard.board[row][col] == 0 and boardState.board[row][col] != 0:
                    end = (row, col)
        return (start, end)

PLAYER = Player_random("me")

def move_random(board, player):
    print("preBoard = ", PLAYER.preBoard)
    print("board = ", BoardState(board))
    return PLAYER.move(board, player)