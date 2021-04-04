import random
import time
import json
import numpy as np
import Genetic_Algorithm_Sudoku as GAS

random.seed(time.time())


def solver(difficult, file):
    given_grid = [[0 for x in range(9)] for y in range(9)]
    store_grid = None

    if difficult == 1:
        with open(file) as f:
            data = json.load(f)

        store_grid = data['Easy']
    elif difficult == 2:
        with open(file) as f:
            data = json.load(f)

        store_grid = data['Medium']
    elif difficult == 3:
        with open(file) as f:
            data = json.load(f)

        store_grid = data['Hard']
    elif difficult == 4:
        with open(file) as f:
            data = json.load(f)

        store_grid = data['Expert']

    given_grid = store_grid[random.randint(0, len(store_grid) - 1)]

    given_grid = np.array(list(given_grid)).reshape((9, 9)).astype(int)
    s = GAS.Sudoku()

    s.load_data(given_grid)
    start_time = time.time()
    generation, solution = s.solve()
    if solution:
        if generation == -1:
            print("Invalid inputs")
            str_print = "Invalid input, please try to generate new game"
        elif generation == -2:
            print("No solution found")
            str_print = "No solution found, please try again"
        else:
            time_elapsed = '{0:6.2f}'.format(time.time() - start_time)
            str_print = "Solution found at generation: " + str(generation) + \
                        "\n" + "Time elapsed: " + str(time_elapsed) + "s"
            print(given_grid)
            print('------------------------------------')
            print(solution.values)

solver(2, "Sudoku_database.json")