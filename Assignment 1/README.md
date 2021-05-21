# Artificial_Intelligence Assignment_1 HCMUT Semester 202

## Member in Team
|NAME|ID Student|
|---|---|
|Lê Quang Tùng|1810784|
|Trương Công Thành|1810766|
|Vũ Minh Dương|1810885|
|Lê Long|1812881|

## Exercise 1 - N puzzle with DFS

[Code](https://github.com/OnceUponATimeMathley/CSE-Artificial_Intelligence_Assignment_1/blob/master/Exercise_1/N-puzzle-DFS.py) -> DFS_Recursive(self, state):

### 1. DFS with Recursion

#### Run Code
    # If you want the available input get in LIST_PUZZLE_DATA
    python3 N-puzzle-DFS.py (numRow = 3) noRandom (numMoves) Recursive 
    # If you want to generate random data
    python3 N-puzzle-DFS.py (numRow) Random (numMoves) Recursive

#### Pseudocode
    DFS(state): 
    # list_action: Storing list direction in recursion
    # The purpose is to print the results
    
    Mark the state is visited
    If state is Goal State: 
        print result in list_action and break
    
    Traverse the possible directions (dir) in LegalMoves(state):
        # Next state when going in the direction (dir)
        next_state = result(state, dir) 
        if next_state is not visited
            push dir in list_action
            DFS(next_state) # Recursive next_state
            pop dir in list_action # Backtracking

### 2. DFS with no Recursion

[Code](https://github.com/OnceUponATimeMathley/CSE-Artificial_Intelligence_Assignment_1/blob/master/Exercise_1/N-puzzle-DFS.py) -> DFS_noRecursive(self, state):

#### Run Code
    # If you want the available input get in LIST_PUZZLE_DATA
    python3 N-puzzle-DFS.py (numRow = 3) noRandom (numMoves) noRecursive 
    # If you want to generate random data
    python3 N-puzzle-DFS.py (numRow) Random (numMoves) noRecursive

#### The reason for this algorithm
    Since the recursive algorithm uses a lot of stack memory, python's stack memory is very small,    
    so the algorithm using recursion fails due to memory overflow, because the depth of the DFS algorithm will
    follows the factorial function of N * N. Hence, we will use recursive elimination to fix this.

## Exercise 2 - Genetic Algorithm For Sudoku

[Code](https://github.com/OnceUponATimeMathley/CSE-Artificial_Intelligence_Assignment_1/tree/master/Exercise_2): Genetic_Algorithm_Sudoku.py, Sudoku.py, Sudoku_database.json

#### Run code

```
python Sudoku.py
```

### GUI

```
1. Fill-predetermined button: Using pencil marking strategy before solving.
2. Solve button: Solving the problem.
3. Reset button: Reset the GUI. Willing to solve another problem.
4. There are 4 mode in order to create initial state of Sudoku.
	a, Easy mode.
	b, Medium mode.
	c, Hard mode.
	d, Expert mode.
```

## Exercise 3 - A* Finding Algorithm

[Code](https://github.com/OnceUponATimeMathley/CSE-Artificial_Intelligence_Assignment_1/tree/master/Exercise_1): A-star.py utils.py

### Run code

```python
python A-star.py
```

### GUI

```
* By click the left mouse button, we can:
	1. Select start cell: orange color
	2. Select goal cell: blue color
	3. Draw to wall: black color
	4. Change the step cost (default: 1 to 5), click 1 button (has ! notation), and draw
	changed cell with step cost: 5: yellow color
	5. Back to default mode, click button 2 (has @ notation).
* By click the right mouse button, we can:
	1. Change the current cell to begin state: white color
* After we has start and goal, other configuration cell, please use space bar to find the path.
* The reset mode will be update in next version, we apologize for the inconvenience.

```





