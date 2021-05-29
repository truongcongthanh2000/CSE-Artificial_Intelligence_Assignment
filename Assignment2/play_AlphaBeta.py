import random
import time
import math
from boardState import BoardState
from play_random import PLAYER

TEACHER = 1 # Quan O
ME = -1 # Quan X
TIMELIMITS = 0.05
INF = math.inf
LIMITS_DEPTH = 6

class Player:
    def __init__(self, str_name = "me"):
        if str_name == "me":
            self.player = 1 # Me
        else:
            self.plyer = -1 # Teacher
        self.preBoard = BoardState()
    
    def __str__(self):
        return self.name

    def move(self, board, player):
        _boardSate = BoardState(board)
        last_move = self.getlast_move(_boardSate)
        type_play = Alpha_Beta()
        best_move = type_play.search(_boardSate, player, self.preBoard, last_move)
        if best_move == None:
            return None
        
        row, col, dir = best_move[0], best_move[1], best_move[2]
        (newrow, newcol) = _boardSate.updateCell(row, col, dir)
        self.preBoard = BoardState([[0 for j in range(_boardSate.n)] for i in range(_boardSate.n)], _boardSate.n)
        self.preBoard.board = [values[:] for values in _boardSate.board]

        start = (row, col)
        end = (newrow, newcol)
        self.preBoard = self.preBoard.change(start, end)
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
        
class Alpha_Beta:
    def __init__(self):
        self.timeStart = time.time()
        
    def TLE(self):
        return time.time() - self.timeStart >= TIMELIMITS
    
    def search(self, board: "BoardState", player, pre_Board : "BoardState", last_move = ()):
        moves = board.listCells_CanMove(player, pre_Board, last_move)
        if len(moves) == 0:
            return None
        if len(moves) == 1:
            return moves[0]
        alpha = -INF
        beta = INF
        best_move = []
        depth = 1
        while not self.TLE():
            for [row, col, dir] in moves:
                newBoard = board.result(row, col, dir)
                value = self.alpha_beta(depth - 1, newBoard, False, alpha, beta, player * (-1), board, last_move)
                if value > alpha:
                    alpha = value
                    best_move.clear()
                if value == alpha:
                    best_move.append([row, col, dir])
                if self.TLE():
                    break
            depth += 1
        
        return random.choice(best_move)

    def alpha_beta(self, depth, board: "BoardState", maxPayer, alpha, beta, player, pre_Board : "BoardState", last_move = ()):
        moves = board.listCells_CanMove(player, pre_Board, last_move)
        if depth == 0 or self.TLE() or len(moves) == 0:
            return board.evaluate(player)
        if maxPayer:
            bestValue = -INF
            for [row, col, dir] in moves:
                newBoard = board.result(row, col, dir)
                value = self.alpha_beta(depth - 1, newBoard, False, alpha, beta, player * (-1), board, last_move)
                if value > bestValue:
                    bestValue = value
                alpha = max(alpha, bestValue)
                if beta <= alpha or self.TLE():
                    break
            return bestValue
        else:
            bestValue = INF
            choost = []
            for [row, col, dir] in moves:
                newBoard = board.result(row, col, dir)
                value = self.alpha_beta(depth - 1, newBoard, True, alpha, beta, player * (-1), board, last_move)
                if value < bestValue:
                    bestValue = value
                    choose = [row, col, dir]
                beta = min(alpha, bestValue)
                if beta <= alpha or self.TLE():
                    break
            return bestValue

PLAYER = Player()

def move(board, player):
    print("preBoard = ", PLAYER.preBoard)
    return PLAYER.move(board, player)