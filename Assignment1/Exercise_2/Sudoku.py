import random
import time
import json
import numpy as np
import Genetic_Algorithm_Sudoku as GAS
import pygame

random.seed(time.time())

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650

grid_before_fill_predetermined = None # Utility to keep track the status of grid to draw

pygame.init()
FONT = pygame.font.SysFont('Corbel', 20, bold=True)


WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku - Genetic Algorithm")


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Tile:
    def __init__(self, row, col, tile_width, total_rows, total_cols):
        self.row = row
        self.col = col
        self.x = col * tile_width
        self.y = row * tile_width
        self.color = WHITE
        self.tile_width = tile_width
        self.total_rows = total_rows
        self.total_cols = total_cols

    def ges_pos(self):
        return self.col, self.row

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.tile_width, self.tile_width))

# Make Tile object for each cell in grid
def make_grid(start_row, start_col, rows, cols, tile_width):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            tile = Tile(start_col + j, start_row + i, tile_width, rows, cols)
            grid[i].append(tile)

    return grid

# Draw the line of each grid
def draw_grid_line(win, start_row, start_col, rows, cols, tile_width):
    line_width = 1
    gap = tile_width
    for i in range(rows + 1):
        if i % 3 == 0:
            line_width = 3
        else:
            line_width = 1
        pygame.draw.line(win, GREY, ((start_row + i) * gap, start_col * gap), ((start_row + i) * gap, (start_col + cols) * gap), width=line_width)
        for j in range(cols + 1):
            if j % 3 == 0:
                line_width = 3
            else:
                line_width = 1
            pygame.draw.line(win, GREY, (start_row * gap, (start_col + j) * gap), ((start_row + rows) * gap, (start_col + j) * gap), width=line_width)

# Draw two grid, button
def draw_grid_tile(win, grid, rows, cols, error_code = 0, given_grid = None, fill_predetermined = False, solving = False):
    win.fill(WHITE)

    tile_width = grid[0][0].tile_width
    start_row_1 = grid[0][0].row
    start_col_1 = grid[0][0].col

    start_row_2 = grid[0][cols].row
    start_col_2 = grid[0][cols].col

    for i in range(rows):
        for j in range(cols):
            grid[i][j].draw(win)
            grid[i][j + cols].draw(win)

    draw_grid_line(win, start_row_1, start_col_1, rows, cols, tile_width)
    draw_grid_line(win, start_row_2, start_col_2, rows, cols, tile_width)

    # Draw button
    pygame.draw.rect(win, ORANGE, (30, 470, 180, 40))
    win.blit(fill_predetermined_button, (40, 480))   # Fill predetermined button

    pygame.draw.rect(win, ORANGE, (30, 525, 70, 40))
    win.blit(solve_button, (40, 535))   # Solve button

    pygame.draw.rect(win, ORANGE, (30, 580, 70, 40))
    win.blit(reset_button, (40, 590))  # Reset button

    win.blit(select_mode, (450, 430)) # Select mode textbox

    pygame.draw.rect(win, ORANGE, (340, 470, 150, 40))
    win.blit(easy_button, (350, 480)) # Easy button

    pygame.draw.rect(win, ORANGE, (340, 530, 150, 40))
    win.blit(medium_button, (350, 540))  # Medium button

    pygame.draw.rect(win, ORANGE, (520, 470, 150, 40))
    win.blit(hard_button, (530, 480))  # Hard button

    pygame.draw.rect(win, ORANGE, (520, 530, 150, 40))
    win.blit(expert_button, (530, 540))  # Expert button


    if error_code != 0:
        if error_code == 1:
            win.blit(message_txt_1, (340, 600))  # Error: Has not been initial
        elif error_code == 2:
            win.blit(message_txt_2, (340, 600))  # Message: Ready to solve
        elif error_code == 3:
            win.blit(message_txt_3, (340, 600))  # Message: Successful
        elif error_code == 4:
            win.blit(message_txt_4, (340, 600))  # Message: Reset successful
        elif error_code == 5:
            win.blit(message_txt_5, (340, 600))  # Message: Waiting solve sudoku.

        global grid_before_fill_predetermined
        # Draw value in grid
        if solving == False:
            if error_code == 5:
                grid_before_fill_predetermined = given_grid.copy()  # Make copy
                # print(grid_before_fill_predetermined)
                return
            if given_grid is not None:

                if grid_before_fill_predetermined is None:  # Keep track before fill_predetermined
                    grid_before_fill_predetermined = given_grid.copy()
                else:
                    # Update the grid_before_fill_predetermined
                    if fill_predetermined == False:
                        check_same = True
                        for i in range(rows):
                            for j in range(cols):
                                if grid_before_fill_predetermined[i][j] != given_grid[i][j]:
                                    check_same = False
                                    break
                            break
                        if check_same == False:
                            grid_before_fill_predetermined = given_grid.copy()

                    # Next logic
                    if error_code == 2 or error_code == 5:
                        GRID_VALUE = pygame.font.SysFont('comicsansms', 20, bold=True)
                        val = None
                        for i in range(rows):
                            for j in range(cols):
                                if grid_before_fill_predetermined[i][j] != 0:
                                    val = GRID_VALUE.render(str(grid_before_fill_predetermined[i][j]), True, BLACK)
                                    x_coordinate = (start_col_1 + j) * tile_width + 14
                                    y_coordinate = (start_row_1 + i) * tile_width + 6
                                    win.blit(val, (x_coordinate, y_coordinate))

                if fill_predetermined == True:
                    # given_grid is updated before, use it instead of grid_before_fill_predetermined
                    GRID_VALUE = pygame.font.SysFont('comicsansms', 20, bold=True)
                    val = None
                    for i in range(rows):
                        for j in range(cols):
                            if given_grid[i][j] != 0:
                                val = GRID_VALUE.render(str(given_grid[i][j]), True, BLACK)
                                x_coordinate = (start_row_2 + j) * tile_width + 14
                                y_coordinate = (start_col_2 + i) * tile_width + 6
                                win.blit(val, (x_coordinate, y_coordinate))
        else:
            if error_code == 3: # Solved completing.
                GRID_VALUE = pygame.font.SysFont('comicsansms', 20, bold=True)
                val = None
                for i in range(rows):
                    for j in range(cols):
                        if grid_before_fill_predetermined[i][j] != 0:
                            val = GRID_VALUE.render(str(grid_before_fill_predetermined[i][j]), True, BLACK)
                            x_coordinate = (start_col_1 + j) * tile_width + 14
                            y_coordinate = (start_row_1 + i) * tile_width + 6
                            win.blit(val, (x_coordinate, y_coordinate))

                for i in range(rows):
                    for j in range(cols):
                        if given_grid[i][j] != 0:
                            val = GRID_VALUE.render(str(given_grid[i][j]), True, BLACK)
                            x_coordinate = (start_row_2 + j) * tile_width + 14
                            y_coordinate = (start_col_2 + i) * tile_width + 6
                            win.blit(val, (x_coordinate, y_coordinate))


    pygame.display.update()


def load_data(difficulty, file):
    store_grid = None

    if difficulty == 1:
        with open(file) as f:
            data = json.load(f)

        store_grid = data['Easy']
    elif difficulty == 2:
        with open(file) as f:
            data = json.load(f)

        store_grid = data['Medium']
    elif difficulty == 3:
        with open(file) as f:
            data = json.load(f)

        store_grid = data['Hard']
    elif difficulty == 4:
        with open(file) as f:
            data = json.load(f)

        store_grid = data['Expert']

    given_grid = store_grid[random.randint(0, len(store_grid) - 1)]

    given_grid = np.array(list(given_grid)).reshape((9, 9)).astype(int)

    return given_grid

if __name__ == '__main__':

    file_name = "Sudoku_database.json"

    solver_GA = GAS.Sudoku()

    TOTAL_ROWS = 9
    TOTAL_COLS = 9
    TILE_WIDTH = 40

    start_row_1 = 1
    start_col_1 = 1

    start_row_2 = 1
    start_col_2 = 11

    fill_predetermined_button = FONT.render('Fill predetermined', True, BLACK)
    solve_button = FONT.render('Solve', True, BLACK)
    reset_button = FONT.render('Reset', True, BLACK)
    select_mode = FONT.render('Select mode', True, BLACK)
    easy_button = FONT.render('Easy mode', True, BLACK)
    medium_button = FONT.render('Medium mode', True, BLACK)
    hard_button = FONT.render('Hard mode', True, BLACK)
    expert_button = FONT.render('Expert mode', True, BLACK)
    message_txt_1 = FONT.render('Message: Select mode before solve', True, BLACK)
    message_txt_2 = FONT.render('Message: Ready to solve', True, BLACK)
    message_txt_3 = FONT.render('Message: Problem is solved!', True, BLACK)
    message_txt_4 = FONT.render('Message: Reset successful!', True, BLACK)
    message_txt_5 = FONT.render('Message: Waiting... to solve the problem!', True, BLACK)


    grid_1 = make_grid(start_row_1, start_col_1, TOTAL_ROWS, TOTAL_COLS, TILE_WIDTH)

    grid_2 = make_grid(start_row_2, start_col_2, TOTAL_ROWS, TOTAL_COLS, TILE_WIDTH)

    combine_grid = []

    for i in range(TOTAL_ROWS):
        combine_grid.append(grid_1[i] + grid_2[i])

    count = 0
    # Grid need to be solve
    given_grid = None

    running = True

    solving = False # Check whether the program is solving the problem.

    fill_predetermined = False

    error_code = 0 # Error code to show the message
    while running:

        # Draw two grid
        draw_grid_tile(WIN, combine_grid, TOTAL_ROWS, TOTAL_COLS, error_code=error_code, \
                       given_grid=given_grid, fill_predetermined=fill_predetermined, solving=solving)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not solving:
                    if 340 <= mouse[0] <= 340 + 150 and 470 <= mouse[1] <= 470 + 40:
                        # Ease mode
                        given_grid = load_data(1, file_name)
                        error_code = 2
                        fill_predetermined = False
                    elif 340 <= mouse[0] <= 340 + 150 and 530 <= mouse[1] <= 530 + 40:
                        # Medium mode
                        given_grid = load_data(2, file_name)
                        error_code = 2
                        fill_predetermined = False
                    elif 520 <= mouse[0] <= 520 + 150 and 470 <= mouse[1] <= 470 + 40:
                        # Hard mode
                        given_grid = load_data(3, file_name)
                        error_code = 2
                        fill_predetermined = False
                    elif 520 <= mouse[0] <= 520 + 150 and 530 <= mouse[1] <= 530 + 40:
                        # Expert mode
                        given_grid = load_data(4, file_name)
                        error_code = 2
                        fill_predetermined = False
                    elif 30 <= mouse[0] <= 30 + 70 and 580 <= mouse[1] <= 580 + 40:
                        # Reset button
                        given_grid = None
                        error_code = 4
                    elif 30 <= mouse[0] <= 30 + 70 and 470 <= mouse[1] <= 525 + 40:
                        # Solve button
                        if given_grid is None:
                            error_code = 1
                        else:
                            error_code = 2
                            solving = True
                    elif 30 <= mouse[0] <= 30 + 180 and 470 <= mouse[1] <= 470 + 40:
                        if given_grid is not None:
                            fill_predetermined = True

                            solver_GA.load_data(given_grid)
                            temp, _ = solver_GA.given_grid.fill_predetermined()
                            given_grid = temp.values # Get value from Fixed object
                else:
                    if 30 <= mouse[0] <= 30 + 70 and 580 <= mouse[1] <= 580 + 40:
                        # Reset button
                        given_grid = None
                        error_code = 4
                        solving = False
        mouse = pygame.mouse.get_pos()

        if solving and count == 0:
            """Handle logic of a program here, solve sudoku by generic algorithm"""
            error_code = 5
            draw_grid_tile(WIN, combine_grid, TOTAL_ROWS, TOTAL_COLS, error_code=error_code, \
                           given_grid=given_grid, fill_predetermined=fill_predetermined, solving=False)
            solver_GA.load_data(given_grid)
            start_time = time.time()
            generation, solution = solver_GA.solve(fill_predetermined) # solution: Chromosome
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
                    error_code = 3
                    given_grid = solution.values
                    fill_predetermined = False
                    count += 1
                    # print(given_grid)
                    # print('------------------------------------')
                    # print(solution.values)

    pygame.quit()
