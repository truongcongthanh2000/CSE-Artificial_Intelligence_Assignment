from hashlib import new
import math

INITIAL_BOARD = [
    [1,   1,   1,   1,   1],
    [1,   0,   0,   0,   1],
    [1,   0,   0,   0,  -1],
    [-1,  0,   0,   0,  -1],
    [-1, -1,  -1,  -1,  -1]
]

import random
import time
import math

TEACHER = 1 # Quan O
ME = -1 # Quan X
TIMELIMITS = 0.05
INF = math.inf
LIMITS_DEPTH = 2

class BoardState:
    """
    This class defines the mechanics of the Board itself.
    """

    def __init__(self, board = INITIAL_BOARD, n = 5):
        """
          Constructs a new board state from an ordering of numbers.

        The configuration of the board is stored in a 2-dimensional
        list (a list of lists) 'board'.
        """
        self.n = n
        self.numPlayer1 = 0
        self.numPlayer2 = 0
        self.board = [values[:] for values in board]
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == -1:
                    self.numPlayer1 += 1
                if self.board[i][j] == 1:
                    self.numPlayer2 += 1

    def isGoal( self ):
        """
          Checks to see if the board is in its goal state.
          board is goal state if board contain only -1, or only 1
          return 0 if not a goal state
          return -1 if board contain only -1
          return 1 if board contain only 1
        """
        if self.numPlayer1 == 0:
            return 1
        if self.numPlayer2 == 0:
            return -1
        return 0
        # d_n1 = 0 # count number(-1)
        # d1 = 0 # count number(1))
        # for row in range( self.n ):
        #     for col in range( self.n ):
        #         if (self.board[row][col] == -1):
        #             d_n1 += 1
        #         if (self.board[row][col] == 1):
        #             d1 += 1
        #         if d_n1 > 0 and d1 > 0:
        #             return 0 # //not goal state
        # if d_n1:
        #     return -1
        # return 1

    def evaluate(self, player):
        if self.isGoal() != 0:
            if player != self.isGoal():
                return INF
            else:
                return -INF
        if player == -1:
            return (self.numPlayer1 - self.numPlayer2) * 1
        else:
            return (self.numPlayer2 - self.numPlayer1) * 1

    def legalMoves( self, row, col):
        """
          Returns a list of legal moves from the current state in cell(row, col).

        Moves consist of moving the cell(row, col) up, down, left or right.
        Special: if (row + col) is even, it can follow the cross
        These are encoded as 'up', 'down', 'left', 'right, and maybe 4 cross respectively.
        -------------
        | 7 | 0 | 1 |
        | 6 | x | 2 |
        | 5 | 4 | 3 |
        -------------
        """
        moves = []
        if(row != 0 and self.board[row - 1][col] == 0):
            moves.append(0)
        if(col != self.n - 1 and self.board[row][col + 1] == 0):
            moves.append(2)
        if(row != self.n - 1 and self.board[row + 1][col] == 0):
            moves.append(4)
        if(col != 0 and self.board[row][col - 1] == 0):
            moves.append(6)
        
        if (row + col) % 2 == 0: # can follow the cross
            if (row != 0 and col != 0 and self.board[row - 1][col - 1] == 0):
                moves.append(7)
            if (row != 0 and col != self.n - 1 and self.board[row - 1][col + 1] == 0):
                moves.append(1)
            if (row != self.n - 1 and col != self.n - 1 and self.board[row + 1][col + 1] == 0):
                moves.append(3)
            if (row != self.n - 1 and col != 0 and self.board[row + 1][col - 1] == 0):
                moves.append(5)

        return moves

    def updatePlayer(self, currentPlayer, cost):
        if currentPlayer == 1:
            self.numPlayer2 += cost
            self.numPlayer1 -= cost
        else:
            self.numPlayer1 += cost
            self.numPlayer2 -= cost
    
    def pair_otherCell(self, row, col):
        ans = []
        if row > 0 and row < self.n - 1:
            ans.append([(row - 1, col), (row + 1, col)])
        if col > 0 and col < self.n - 1:
            ans.append([(row, col - 1), (row, col + 1)])
        if (row + col) % 2 == 0:
            if row > 0 and row < self.n - 1 and col > 0 and col < self.n - 1:
                ans.append([(row - 1, col - 1), (row + 1, col + 1)])
                ans.append([(row - 1, col + 1), (row + 1, col - 1)])
        return ans

    def ganh(self, row, col):
        player = self.board[row][col] # current player
        assert player != 0, "player failed in ganh with cell(" + str(row) + ", " + str(col) + ")"

        list_pairOtherCell = self.pair_otherCell(row, col)
        for pair in list_pairOtherCell:
            left = pair[0]
            right = pair[1]
            if self.board[left[0]][left[1]] * (-1) == player and self.board[right[0]][right[1]] * (-1) == player:
                self.board[left[0]][left[1]] = player
                self.board[right[0]][right[1]] = player
                self.updatePlayer(player, 2)

    def chet(self, row, col):
        player = self.board[row][col] # current player
        assert player != 0, "player failed in chet with cell(" + str(row) + ", " + str(col) + ")"

        isVisited = [[0 for j in range(self.n)] for i in range(self.n)]
        queue = []

        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == 0:
                    queue.append([i, j])
                    isVisited[i][j] == 1
        while len(queue) > 0:
            last_element = queue.pop()
            x = last_element[0]
            y = last_element[1]
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    if (x + y) % 2 == 1 and dx != 0 and dy != 0:
                        continue
                    next_x = x + dx
                    next_y = y + dy
                    if next_x >= 0 and next_x < self.n and next_y >= 0 and next_y < self.n:
                        if isVisited[next_x][next_y] == 0 and self.board[next_x][next_y] != player:
                            queue.append([next_x, next_y])
                            isVisited[next_x][next_y] = 1

        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] * (-1) == player and isVisited[i][j] == 0:
                    self.board[i][j] = player
                    self.updatePlayer(player, 1)

    def change(self, start, end): 
        """
            Returns a new boardState with the current state and move from start to end
        """
        newBoard = BoardState([[0 for j in range(self.n)] for i in range(self.n)], self.n)
        newBoard.board = [values[:] for values in self.board]
        newBoard.numPlayer1 = self.numPlayer1
        newBoard.numPlayer2 = self.numPlayer2

        # And update it to reflect the move
        row, col = start[0], start[1]
        newrow, newcol = end[0], end[1]

        newBoard.board[row][col] = self.board[newrow][newcol]
        newBoard.board[newrow][newcol] = self.board[row][col]
        
        newBoard.ganh(newrow, newcol)
        newBoard.chet(newrow, newcol)
        return newBoard

    def updateCell(self, row, col, move):
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
        return (newrow, newcol)

    def result(self, row, col, move):
        """
          Returns a new boardState with the current state and cell(row, col)
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        -------------
        | 7 | 0 | 1 |
        | 6 | x | 2 |
        | 5 | 4 | 3 |
        -------------
        """
        start = (row, col)
        end = self.updateCell(row, col, move)

        return self.change(start, end)

    def listCells_canMove_withoutBay(self, player):
        canMove = []
        for row in range(self.n):
            for col in range(self.n):
                if self.board[row][col] == player:
                    list_dir = self.legalMoves(row, col)
                    for dir in list_dir:
                        canMove.append([row, col, dir])
        return canMove

    def listCells_CanMove(self, player, pre_Board : "BoardState", last_move):
        if len(last_move) == 2 and last_move[0] != last_move[1] and pre_Board.numPlayer1 == self.numPlayer1 and pre_Board.numPlayer2 == self.numPlayer2:
            position_open = last_move[0] # vi tri mo ? 
            canMove = []
            listBay = []
            for row in range(self.n):
                for col in range(self.n):
                    if self.board[row][col] == player: 
                        list_dir = self.legalMoves(row, col)
                        for dir in list_dir:
                            (newrow, newcol) = self.updateCell(row, col, dir)
                            if newrow == position_open[0] and newcol == position_open[1]:
                                list_pairOtherSide = self.pair_otherCell(newrow, newcol)
                                for [left, right] in list_pairOtherSide:
                                    if left == (row, col) or right == (row, col):
                                        continue
                                    if self.board[left[0]][left[1]] * (-1) == player and self.board[right[0]][right[1]] * (-1) == player:              
                                        listBay.append([row, col, dir])
                                        break
                            canMove.append([row, col, dir])
            if len(listBay) > 0:
                return listBay
            else:
                return canMove
        else:
            return self.listCells_canMove_withoutBay(player)

    # Utilities for comparison and display
    def __eq__(self, other):
        """
            Overloads '==' such that two boardState with the same configuration
          are equal.

        """
        for row in range( self.n ):
            if self.board[row] != other.board[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.board))

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        lines = []
        horizontalLine = ('-' * (26))
        lines.append(horizontalLine)
        for row in self.board:
            rowLine = '|'
            for col in row:
                if col == -1:
                    col = 'O'
                if col == 0:
                    col = '-'
                if col == 1:
                    col = 'X'
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()
        
import random
"""
    -------------
    | 7 | 0 | 1 |
    | 6 | x | 2 |
    | 5 | 4 | 3 |
    -------------
"""

class Player:
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
        type_play = Alpha_Beta()
        best_move = type_play.search(_boardSate, player, self.preBoard, last_move)
        if best_move == None:
            return None
        
        row, col, dir = best_move[0], best_move[1], best_move[2]
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
        depth = LIMITS_DEPTH
        while not self.TLE() and depth <= LIMITS_DEPTH:
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
                if self.TLE():
                    break
            return bestValue
        else:
            bestValue = INF
            for [row, col, dir] in moves:
                newBoard = board.result(row, col, dir)
                value = self.alpha_beta(depth - 1, newBoard, True, alpha, beta, player * (-1), board, last_move)
                if value < bestValue:
                    bestValue = value
                if self.TLE():
                    break
            return bestValue

PLAYER = Player()

def move(board, player, remain_time):
    return PLAYER.move(board, player)
