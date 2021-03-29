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

# https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
def isSolvable(puzzle):
    n = len(puzzle)
    arr = [puzzle[i][j] for i in range(n) for j in range(n)]
    print("arr = ", arr)
    invCount = count_NumInversion(arr)
    if n % 2:
        if invCount and 1:
            return False
        else:
            return True
    else:
        pos = 0
        for i in range(n):
            for j in range(n):
                if puzzle[i][j] == 0:
                    pos = n - i
                    break
        if pos % 2:
            if invCount and 1:
                return False
            else:
                return True
        else:
            if invCount and 1:
                return True
            else:
                return False

def count_NumInversion(arr):
    n = len(arr)
    ST = SegmentTree(n)
    ans = 0
    for x in arr:
        num = ST.number_Bigger(x)
        ans += num
        ST.add(x)
    return ans

def gen(n = 4):
    perm = np.random.permutation(n * n)
    print(perm)
    print(count_NumInversion(perm))
    ans = [[perm[i * n + j] for j in range(n)] for i in range(n)]
    return ans

def DFS(cur, goal):
    return -1

def main():
    n = 4
    puzzle = gen(n)
    print(puzzle)
    print(isSolvable(puzzle))

    goal = [i for i in range(1, n * n)]
    goal.append(0)
    print(goal)


if __name__ == '__main__':
    start = timeit.default_timer()

    numTest = 1
    while numTest:
        main()
        numTest -= 1

    stop = timeit.default_timer()
    print('Time: ', stop - start, file = sys.stderr)