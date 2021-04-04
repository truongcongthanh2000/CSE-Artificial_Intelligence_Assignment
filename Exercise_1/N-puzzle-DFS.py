import sys
import math
import timeit
from collections import Counter
from random import randint
from numpy import random
import numpy as np

class SegmentTree:
    def __init__(self, n):
        self.n = n
        self.IT = [0 for i in range(n * 4)]
    
    def update(self, i, L, R, u):
        if (L > u) or (R < u):
            return None
        if L == R:
            self.IT[i] = 1
            return None
        mid = (L + R) >> 1
        self.update(i << 1, L, mid, u)
        self.update(i << 1 | 1, mid + 1, R, u)
        self.IT[i] = self.IT[i << 1] + self.IT[i << 1 | 1]
        
    def count(self, i, L, R, u, v):
        if (L > v) or (R < u):
            return 0
        if L >= u and R <= v:
            return self.IT[i]
        mid = (L + R) >> 1
        left = self.count(i << 1, L, mid, u, v)
        right = self.count(i << 1 | 1, mid + 1, R, u, v)
        return left + right
    
    def add(self, x):
        self.update(1, 0, self.n - 1, x)

    def number_Bigger(self, x):
        return self.count(1, 0, self.n - 1, x + 1, self.n - 1)


def count_NumInversion(arr):
    n = len(arr)
    invCount = 0
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > 0 and arr[j] > 0 and arr[j] < arr[i]:
                invCount += 1
    return invCount
    # ST = SegmentTree(n)
    # ans = 0
    # for x in arr:
    #     if x > 0:
    #         num = ST.number_Bigger(x)
    #         ans += num
    #     ST.add(x)
    # return ans

# How to check if an instance of N puzzle is solvable
# https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
def isSolvable(puzzle):
    sz = len(puzzle)
    n = int(math.sqrt(sz))
    assert n * n == sz, "isSolvable -> sqrt: failed"
    # arr = [puzzle[i][j] for i in range(n) for j in range(n)]
    # print("arr = ", arr)
    # invCount = count_NumInversion(arr)
    invCount = count_NumInversion(puzzle)
    if n % 2:
        if invCount % 2:
            return False
        else:
            return True
    else:
        pos = 0
        for i in range(n):
            for j in range(n):
                if puzzle[i * n + j] == 0:
                    pos = n - i
                    break
        if pos % 2:
            if invCount % 2:
                return False
            else:
                return True
        else:
            if invCount % 2:
                return True
            else:
                return False

def gen(n = 4):
    perm = np.random.permutation(n * n)
    return list(perm)
    # print(perm)
    # print(count_NumInversion(perm))
    # ans = [[perm[i * n + j] for j in range(n)] for i in range(n)]
    # return ans


def printTable(arr):
    sz = len(arr)
    n = int(math.sqrt(sz))
    assert n * n == sz, "printTable -> sqrt: failed"
    for i in range(n):
        for j in range(n):
            print(arr[i * n + j], end = ' ')
        print()

list_puzzle = []

def printPath():
    print("Result: " )
    number_Puzzle = len(list_puzzle)
    print("Start Puzzle:")
    printTable(list_puzzle[0][0])
    print()

    if number_Puzzle == 1:
        print("Final Puzzle:")
        printTable(list_puzzle[0][0])
        return None

    for i in range(1, number_Puzzle - 1):
        print("Swap: " + str(list_puzzle[i - 1][1]) + ", " + str(list_puzzle[i - 1][2]))
        printTable(list_puzzle[i][0])
        print()
    
    print("Swap: " + str(list_puzzle[number_Puzzle - 2][1]) + ", " + str(list_puzzle[number_Puzzle - 2][2]) + " -> Final Puzzle:")
    printTable(list_puzzle[number_Puzzle - 1][0])

    return None

dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]

def inTable(x, y, n):
    return x >= 0 and x < n and y >= 0 and y < n

def check_if_exactly_equal(list_1, list_2):
    # check if both the lists are of same size
    if len(list_1) != len(list_2):
        return False
    # create a zipped object from 2lists
    final_list = zip(list_1, list_2)
    # iterate over the zipped object
    for elem in final_list:
        if elem[0] != elem[1]:
            return False
    return True

class MapList:
    mod = 10**6 + 3
    adj = [[] for i in range(mod)]
    base = 311

    def hash(self, cur_list):
        ans = 0
        for x in cur_list:
            ans = (ans * self.base + x) % self.mod 
        return ans
    
    def insert(self, cur_list):
        key = self.hash(cur_list)
        self.adj[key].append(cur_list)
    
    def find(self, cur_list):
        key = self.hash(cur_list)
        for lst in self.adj[key]:
            if check_if_exactly_equal(lst, cur_list):
                return True
            # if lst == cur_list:
            #     return True
        return False

isVisited = MapList()
def DFS(cur, goal, p_index, n):
    # print(cur)
    isVisited.insert(cur)
    list_puzzle.append([cur, -1, -1])
    
    if check_if_exactly_equal(cur, goal):
        printPath()
        return True

    p0 = p_index[0]
    x = p0 // n
    y = p0 % n
    for dir in range(4):
        next_x = x + dx[dir]
        next_y = y + dy[dir]
        if inTable(next_x, next_y, n):
            idx = next_x * n + next_y
            # assert idx >= 0 and idx < n * n, "Out of Index"
            # assert len(cur) == n * n, "Size Array Not Equal N x N"
            value = cur[idx]
            
            new_cur = cur.copy()
            new_cur[x * n + y], new_cur[idx] = new_cur[idx], new_cur[x * n + y]
            p_index[0], p_index[value] = p_index[value], p_index[0]
            list_puzzle[len(list_puzzle) - 1][1] = 0
            list_puzzle[len(list_puzzle) - 1][2] = value
            
            checkVisited = isVisited.find(new_cur)
            if checkVisited == False and DFS(new_cur, goal, p_index, n):
                return True

            p_index[0], p_index[value] = p_index[value], p_index[0]
            list_puzzle[len(list_puzzle) - 1][1] = -1
            list_puzzle[len(list_puzzle) - 1][2] = -1
    
    list_puzzle.pop()
    return False

list_canSolved = [
    [1, 2, 3, 4, 6, 0, 7, 5, 8], 
    [7, 5, 8, 3, 0, 1, 2, 6, 4]
]
def main():
    print(sys.getrecursionlimit()) # = 1000
    # sys.setrecursionlimit(12345678) 

    n = 3
    puzzle = gen(n)
    # puzzle = [1, 2, 3, 4, 6, 0, 7, 5, 8]
    p_index = [0 for i in range(n * n)]
    for i in range(n * n):
        p_index[puzzle[i]] = i
    print(puzzle)

    canSolve = isSolvable(puzzle)
    print(canSolve)
    printTable(puzzle)

    goal = [i for i in range(1, n * n)]
    goal.append(0)
    print(goal)

    assert DFS(puzzle, goal, p_index, n) == canSolve, "Error to Solve: " + str(canSolve)


if __name__ == '__main__':
    start = timeit.default_timer()

    numTest = 1
    while numTest:
        main()
        numTest -= 1

    stop = timeit.default_timer()
    print('Time: ', stop - start, file = sys.stderr)