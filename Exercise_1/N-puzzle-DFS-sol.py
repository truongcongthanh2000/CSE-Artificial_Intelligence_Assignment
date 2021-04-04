import sys
import math
import timeit
from collections import Counter
from random import randint
import numpy as np
import random

# 2 way to run code:
# python N-puzzle-DFS-sol.py (numRow) noRandom (numMoves))
# python N-puzzle-DFS-sol.py (numRow) Random numMoves

class N_PuzzleState:
    """
    The Eight Puzzle is described in the course textbook on
    page 64.

    This class defines the mechanics of the puzzle itself.  The
    task of recasting this puzzle as a search problem is left to
    the EightPuzzleSearchProblem class.
    """

    def __init__(self, numbers, n):
        """
          Constructs a new eight puzzle from an ordering of numbers.

        numbers: a list of integers from 0 to 8 representing an
          instance of the eight puzzle.  0 represents the blank
          space.  Thus, the list

            [1, 0, 2, 3, 4, 5, 6, 7, 8]

          represents the eight puzzle:
            -------------
            | 1 |   | 2 |
            -------------
            | 3 | 4 | 5 |
            -------------
            | 6 | 7 | 8 |
            ------------

        The configuration of the puzzle is stored in a 2-dimensional
        list (a list of lists) 'cells'.
        """
        self.cells = []
        numbers = numbers[:] # Make a copy so as not to cause side-effects.
        numbers.reverse()
        self.n = n
        for row in range( self.n ):
            self.cells.append( [] )
            for col in range( self.n ):
                self.cells[row].append( numbers.pop() )
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col

    def isGoal( self ):
        """
          Checks to see if the puzzle is in its goal state.
          For example, n = 3:
            -------------
            |   | 1 | 2 |
            -------------
            | 3 | 4 | 5 |
            -------------
            | 6 | 7 | 8 |
            -------------

        >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).isGoal()
        True

        >>> EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).isGoal()
        False
        """
        current = 0
        for row in range( self.n ):
            for col in range( self.n ):
                if current != self.cells[row][col]:
                    return False
                current += 1
        return True

    def legalMoves( self ):
        """
          Returns a list of legal moves from the current state.

        Moves consist of moving the blank space up, down, left or right.
        These are encoded as 'up', 'down', 'left' and 'right' respectively.

        >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).legalMoves()
        ['down', 'right']
        """
        moves = []
        row, col = self.blankLocation
        if(row != 0):
            moves.append('up')
        if(row != self.n - 1):
            moves.append('down')
        if(col != 0):
            moves.append('left')
        if(col != self.n - 1):
            moves.append('right')
        return moves

    def result(self, move):
        """
          Returns a new eightPuzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        """
        row, col = self.blankLocation
        if(move == 'up'):
            newrow = row - 1
            newcol = col
        elif(move == 'down'):
            newrow = row + 1
            newcol = col
        elif(move == 'left'):
            newrow = row
            newcol = col - 1
        elif(move == 'right'):
            newrow = row
            newcol = col + 1
        else:
            raise "Illegal Move"

        # Create a copy of the current eightPuzzle
        newPuzzle = N_PuzzleState([0 for i in range(self.n * self.n)], self.n)
        newPuzzle.cells = [values[:] for values in self.cells]
        # And update it to reflect the move
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = self.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle

    # Utilities for comparison and display
    def __eq__(self, other):
        """
            Overloads '==' such that two eightPuzzles with the same configuration
          are equal.

          >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]) == \
              EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).result('left')
          True
        """
        for row in range( self.n ):
            if self.cells[row] != other.cells[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        lines = []
        horizontalLine = ('-' * (13))
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = ' '
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()

class N_PuzzleStorage:
    def __init__(self):
        self.isVisited = {}
    
    def add(self, state):
        # print("Add: ")
        # print(state)
        self.isVisited[state] = True
    
    def isVisit(self, state):
        if state in self.isVisited:
            return True
        else:
            return False

class N_PuzzleSearchProblem():
    """
      Implementation of a SearchProblem for the  Eight Puzzle domain

      Each state is represented by an instance of an eightPuzzle.
    """
    def __init__(self, puzzle, n):
        "Creates a new EightPuzzleSearchProblem which stores search information."
        self.puzzle = puzzle
        self.n = n
        self.MapPuzzle = N_PuzzleStorage()
        self.list_action = []

    def getStartState(self):
        return self.puzzle

    def isGoalState(self,state):
        return state.isGoal()

    def DFS(self, state):
        # print("DFS = ")
        # print(state)
        self.MapPuzzle.add(state)
        if self.isGoalState(state):
            return True

        for a in state.legalMoves():
            # print(a)
            successor = state.result(a)
            # print(successor)
            if self.MapPuzzle.isVisit(successor) == False:
                self.list_action.append(a)
                if self.DFS(successor):
                    return True
                self.list_action.pop()
        return False

    def getSuccessors(self,state):
        """
          Returns list of (successor, action, stepCost) pairs where
          each succesor is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ
    
    def getListActions(self):
        return self.list_action

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)

def getSuccessors(self,state):
    """
        Returns list of (successor, action, stepCost) pairs where
        each succesor is either left, right, up, or down
        from the original state and the cost is 1.0 for each
    """
    succ = []
    for a in state.legalMoves():
        succ.append((state.result(a), a, 1))
    return succ

LIST_PUZZLE_DATA = [[1, 0, 2, 3, 4, 5, 6, 7, 8],
                     [1, 7, 8, 2, 3, 4, 5, 6, 0],
                     [4, 3, 2, 7, 0, 5, 1, 6, 8],
                     [5, 1, 3, 4, 0, 2, 6, 7, 8],
                     [1, 2, 5, 7, 6, 8, 0, 4, 3],
                     [0, 3, 1, 6, 8, 2, 7, 5, 4]]

def loadEightPuzzle(puzzleNumber):
    """
      puzzleNumber: The number of the eight puzzle to load.

      Returns an eight puzzle object generated from one of the
      provided puzzles in EIGHT_PUZZLE_DATA.

      puzzleNumber can range from 0 to 5.

      >>> print(loadEightPuzzle(0))
      -------------
      | 1 |   | 2 |
      -------------
      | 3 | 4 | 5 |
      -------------
      | 6 | 7 | 8 |
      -------------
    """
    puzzle = LIST_PUZZLE_DATA[puzzleNumber]
    n = int(math.sqrt(len(puzzle)))
    return N_PuzzleState(puzzle, n)

def createRandomN_Puzzle(n, moves = 100):
    """
      moves: number of random moves to apply

      Creates a random eight puzzle by applying
      a series of 'moves' random moves to a solved
      puzzle.
    """
    puzzle = N_PuzzleState([i for i in range(n * n)], n)
    for i in range(moves):
        # Execute a random legal move
        puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle

def main(n, isRandom, moves):
    print(sys.getrecursionlimit()) # = 1000
    sys.setrecursionlimit(12345678) 

    if isRandom == False:
        n = 3
        # choose = random.randint(0, 5)
        choose = 0
        print("Choose puzzle = ", choose)
        problem = N_PuzzleSearchProblem(loadEightPuzzle(choose), n)
    else:
        problem = N_PuzzleSearchProblem(createRandomN_Puzzle(n, moves), n)

    startState = problem.getStartState()

    print(startState)

    if problem.DFS(startState):
        print("Problem is Solvable: ")
        path = problem.getListActions()

        i = 1
        for a in path:
            startState = startState.result(a)
            print('After %d move%s: %s' % (i, ("", "s")[i>1], a))
            print(startState)

            i += 1

if __name__ == '__main__':
    start = timeit.default_timer()

    numTest = 1
    while numTest:
        main(int(sys.argv[1]), sys.argv[2] == "Random", int(sys.argv[3]))
        numTest -= 1

    stop = timeit.default_timer()
    print('Time: ', stop - start, file = sys.stderr)