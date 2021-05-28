import random
from boardState import BoardState

"""
    -------------
    | 7 | 0 | 1 |
    | 6 | x | 2 |
    | 5 | 4 | 3 |
    -------------
"""

def move(board, player):
    _boardState = BoardState(board)
    if _boardState.isGoal():
        return None
    canMove = _boardState.listCells_CanMove(player)
    if len(canMove) == 0:
        return None
    cell = random.choice(canMove)
    move = random.choice(_boardState.legalMoves(cell[0], cell[1]))
    row, col = cell[0], cell[1]

    if(move == 0):
        newrow = row - 1
        newcol = col
    elif(move == 1):
        newrow = row - 1
        newcol = col + 1
    elif(move == 2):
        newrow = row
        newcol = col + 1
    elif(move == 3):
        newrow = row + 1
        newcol = col + 1
    elif(move == 4):
        newrow = row + 1
        newcol = col
    elif(move == 5):
        newrow = row + 1
        newcol = col - 1
    elif(move == 6):
        newrow = row
        newcol = col - 1
    elif(move == 7):
        newrow = row - 1
        newcol = col - 1
    else:
        raise "Illegal Move"

    start = (4 - row, col)
    end = (4 - newrow, newcol)

    return (start, end)