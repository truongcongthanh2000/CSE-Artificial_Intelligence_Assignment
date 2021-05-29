import sys
import math
import timeit
from collections import Counter
from random import randint
import numpy as np
import random
from boardState import BoardState
"""
    -------------
    | 7 | 0 | 1 |
    | 6 | x | 2 |
    | 5 | 4 | 3 |
    -------------
"""
def test():
    if True:   
        print("Test Ganh 1")
        test_board = [
            [1,   0,   1,   1,   1],
            [1,   1,   0,   0,   1],
            [-1,  0,   0,   1,   0],
            [-1, -1,  -1,   0,  -1],
            [-1,  0,   0,  -1,  -1]
        ]
        a = BoardState(test_board)
        row, col = 2, 3
        dir = 4
        new_a = a.result(row, col, dir)
        print(a)
        print("move with cell(" + str(row) + ", " + str(col) + ") and dir = " + str(dir))
        print(new_a)

    if True:  
        print("Test Ganh 2")
        test_board = [
            [0,   0,   1,   0,   1],
            [-1, -1,   0,   0,   1],
            [-1, -1,  -1,   0,   0],
            [-1,  0,  -1,   1,   1],
            [-1,  1,  -1,   0,   1]
        ]
        a = BoardState(test_board)
        row, col = 4, 1
        dir = 0
        new_a = a.result(row, col, dir)
        print(a)
        print("move with cell(" + str(row) + ", " + str(col) + ") and dir = " + str(dir))
        print(new_a)

    if True:  
        print("Test Chet 1")
        test_board = [
            [-1,  0,   1,   0,   1],
            [ 0,  -1,  0,   0,   1],
            [ 1,  1,  -1,   0,   0],
            [-1, -1,   1,   1,   1],
            [-1,  0,   0,  -1,  -1]
        ]
        a = BoardState(test_board)
        row, col = 0, 0
        dir = 4
        new_a = a.result(row, col, dir)
        print(a)
        print("move with cell(" + str(row) + ", " + str(col) + ") and dir = " + str(dir))
        print(new_a)

    print("Test ALL: ")
    board = [
        [1,   1,   1,   1,   1],
        [1,   0,   0,   0,   1],
        [1,   0,   0,   0,  -1],
        [-1,  0,   0,   0,  -1],
        [-1, -1,  -1,  -1,  -1]
    ]
    a = BoardState(board)
    canMove = a.listCells_CanMove(-1)
    cell = random.choice(canMove)
    dir = random.choice(a.legalMoves(cell[0], cell[1]))
    row, col = cell[0], cell[1]
    print(a)
    print(canMove)
    print("cell = ", row, col)
    print("dir = ", dir)
    new_a = a.result(row, col, dir)
    print(new_a)

def main():
    startTime = timeit.default_timer()

    from play_random import move
    board = [
        [1,   1,   1,   1,   1],
        [1,   0,   0,   0,   1],
        [1,   0,   0,   0,  -1],
        [-1,  0,   0,   0,  -1],
        [-1, -1,  -1,  -1,  -1]
    ]
    _boardState = BoardState(board)
    player = -1
    PlayRound = 0

    print("Init Board", _boardState)
    while timeit.default_timer() - startTime < 3.0 and _boardState.isGoal() == 0:
        PlayRound += 1
        print("Round", PlayRound)
        (start, end) = move(_boardState.board, player)
        _boardState = _boardState.change(start, end)
        print("Result: ", _boardState)
        
        player *= -1

if __name__ == '__main__':
    start = timeit.default_timer()

    numTest = 1
    while numTest:
        # test()
        main()
        numTest -= 1

    stop = timeit.default_timer()
    print('Time: ', stop - start, file = sys.stderr)
