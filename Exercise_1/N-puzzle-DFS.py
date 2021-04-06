import sys
import math
import timeit
from collections import Counter
from random import randint
import numpy as np
import random

# 2 way to run code:
# python N-puzzle-DFS-sol.py (numRow) noRandom (numMoves) ('Recursive', 'noRecursive')
# python N-puzzle-DFS-sol.py (numRow) Random (numMoves) ('Recursive', 'noRecursive')
# best Solution: Choose noRecursive to avoid use lot of memory

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

        >>> N_PuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).isGoal()
        True

        >>> N_PuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).isGoal()
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

        >>> N_PuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).legalMoves()
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

          >>> N_PuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]) == \
              N_PuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).result('left')
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

# https://www.geeksforgeeks.org/stack-in-python/
# Python program to demonstrate
# stack implementation using a linked list.
# node class
class Node:
   def __init__(self, value):
      self.value = value
      self.next = None
 
class Stack:
    
   # Initializing a stack.
   # Use a dummy node, which is
   # easier for handling edge cases.
   def __init__(self):
      self.head = Node("head")
      self.size = 0
 
   # String representation of the stack
   def __str__(self):
      cur = self.head.next
      out = ""
      while cur:
         out += str(cur.value) + "->"
         cur = cur.next
      return out[:-3]  
 
   # Get the current size of the stack
   def getSize(self):
      return self.size
    
   # Check if the stack is empty
   def isEmpty(self):
      return self.size == 0
    
   # Get the top item of the stack
   def peek(self):
       
      # Sanitary check to see if we
      # are peeking an empty stack.
      if self.isEmpty():
         raise Exception("Peeking from an empty stack")
      return self.head.next.value
 
   # Push a value into the stack.
   def push(self, value):
      node = Node(value)
      node.next = self.head.next
      self.head.next = node
      self.size += 1
      
   # Remove a value from the stack and return.
   def pop(self):
      if self.isEmpty():
         raise Exception("Popping from an empty stack")
      remove = self.head.next
      self.head.next = self.head.next.next
      self.size -= 1
      return remove.value

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
        self.n_DFS = 0

    def getStartState(self):
        return self.puzzle

    def isGoalState(self,state):
        return state.isGoal()

    def DFS_noRecursive(self, state):
        stk = Stack()
        stk.push(state)

        while stk.isEmpty() == False:
            cur = stk.pop()
            self.MapPuzzle.add(cur)

            if self.isGoalState(cur):
                return True
            hasChoose = False
            for a in cur.legalMoves():
                successor = cur.result(a)
                if self.MapPuzzle.isVisit(successor) == False:
                    self.list_action.append(a)
                    stk.push(cur)
                    stk.push(successor)
                    hasChoose = True
                    break
            if hasChoose == False:
                if len(self.list_action) > 0:
                    self.list_action.pop()
    
    def DFS_Recursive(self, state):
        self.n_DFS += 1
        # print("DFS = ", self.n_DFS)
        # print(state)
        self.MapPuzzle.add(state)
        if self.isGoalState(state):
            return True

        if self.n_DFS < 3500: # Magic!
            for a in state.legalMoves():
                # print(a)
                successor = state.result(a)
                # print(successor)
                if self.MapPuzzle.isVisit(successor) == False:
                    self.list_action.append(a)
                    if self.DFS_Recursive(successor):
                        return True
                    self.list_action.pop()
        self.n_DFS -= 1
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
    print(puzzle, n)
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

def main(n, isRandom, moves, isRecursive):
    print("Number Recursion = ", sys.getrecursionlimit()) # = 1000
    sys.setrecursionlimit(12345678) 

    if isRandom == False:
        n = 3
        choose = random.randint(0, 5)
        # choose = 1 # Thay đổi chọn puzzle 1 -> đệ quy lâu hơn

        print("Choose puzzle = ", choose, file = sys.stderr)
        problem = N_PuzzleSearchProblem(loadEightPuzzle(choose), n)
    else:
        problem = N_PuzzleSearchProblem(createRandomN_Puzzle(n, moves), n)

    startState = problem.getStartState()

    print(startState)
    
    canSolved = False
    if isRecursive == True:
        canSolved = problem.DFS_Recursive(startState)
    else:
        canSolved = problem.DFS_noRecursive(startState)

    if canSolved:
        print("Problem is Solvable: ")
        path = problem.getListActions()

        i = 1
        for a in path:
            startState = startState.result(a)
            print('After %d move%s: %s' % (i, ("", "s")[i>1], a))
            print(startState)

            i += 1
    else:
        print("Problem may have no solution: ")

if __name__ == '__main__':
    start = timeit.default_timer()

    numTest = 1
    while numTest:
        main(int(sys.argv[1]), sys.argv[2] == "Random", int(sys.argv[3]), sys.argv[4] == "Recursive")
        numTest -= 1

    stop = timeit.default_timer()
    print('Time: ', stop - start, file = sys.stderr)