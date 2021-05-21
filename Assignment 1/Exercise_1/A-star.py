import pygame
from Exercise_1.utils import *

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("A* Path Finding Algorithm")

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
        self.neighbors = []
        self.width = tile_width
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.step_cost = 1
        self.path_cost = 0

    def get_pos(self):
        return self.col, self.row

    # Closed list
    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    # Wall
    def is_barrier(self):
        return self.color == BLACK

    # Start point
    def is_start(self):
        return self.color == ORANGE

    # End point
    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def is_white(self):
        return self.color == WHITE

    def is_increase_size(self):
        return self.color == YELLOW

    def make_increase_size(self):
        self.color = YELLOW
        self.step_cost = 5

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = [] #Reset neighbors
        # UP
        if self.row > 0 and self.row < self.total_rows and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        #DOWN
        if self.row >= 0 and self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        #LEFT
        if self.col > 0 and self.col < self.total_cols and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

        #RIGHT
        if self.col >= 0 and self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])


    def __lt__(self, other):
        return False

    def __eq__(self, other):
        # print("OK")
        if other:
            return (self.row == other.row and self.col == other.col)
        return False

    def __ne__(self, other):

        if other:
            return (self.row != other.row or self.col != other.col)
        return True

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        hash_value = "Tile location: ({:d}, {:d})".format(self.row, self.col)
        return hash_value


def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)

def make_grid(rows, cols, screen_width, screen_height):
    grid = []
    gap = screen_width // cols
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            tile = Tile(i, j, gap, rows, cols)
            grid[i].append(tile)
    return grid

def draw_screen_line(win, rows, cols, screen_width, screen_height):
    gap = screen_width // cols
    for i in range(rows):
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, screen_width))
        for j in range(cols):
            pygame.draw.line(win, GREY, (0, j * gap), (screen_height, j * gap))


def draw_tile(win, grid, rows, cols, screen_width, screen_height):
    win.fill(WHITE)

    for i in range(rows):
        for j in range(cols):
            grid[i][j].draw(win)

    draw_screen_line(win, rows, cols, screen_width, screen_height)
    pygame.display.update()


def get_click_pos(pos, cols, screen_width):
    gap = screen_width // cols
    x = pos[0] // gap
    y = pos[1] // gap
    return y, x


def draw_path(path, current, draw_tile):
    while current in path:
        current = path[current]
        if current:
            current.make_path()
        draw_tile()


def A_Star_Algorithm(draw_tile, grid, start, end):
    fringe = PriorityQueue()
    frontier = Counter()
    explored = Counter()

    path = {start : None}

    #Initial
    fringe.push(start, heuristic(start.get_pos(), end.get_pos()))
    frontier[hash(start)] = start
    start.make_open()


    while not fringe.isEmpty():
        current = fringe.pop()
        explored[hash(current)] = current # Add to explored list
        current.make_closed()
        frontier.pop(hash(current), None) # Remove from frontier
        # print("Current", current.row, current.col, current_path_cost)
        if current == end:
            draw_path(path, end, draw_tile)
            start.make_start()
            end.make_end()
            return True


        for neighbor in current.neighbors:
            # print("Neighbor", neighbor.row, neighbor.col)
            key = hash(neighbor)

            if explored[key] == 0:
                # new_neighbor = Tile(neighbor.row, neighbor.col, neighbor.width, neighbor.total_rows, neighbor.total_cols)
                neighbor.path_cost += neighbor.step_cost
                new_path_cost = neighbor.path_cost # The default step cost: 1, will be change
                if frontier[key] == 0:
                    path[neighbor] = current
                    neighbor.make_open()
                    f_cost = new_path_cost + heuristic(neighbor.get_pos(), end.get_pos())
                    # print(f_cost, neighbor.row, neighbor.col)
                    fringe.push(neighbor, f_cost)
                    frontier[key] = neighbor
                else:
                    old_path_cost = neighbor.path_cost
                    if old_path_cost > new_path_cost:
                        fringe.update(neighbor, new_path_cost)
                        frontier.pop(hash(neighbor), None)
                        frontier[hash(neighbor)] = neighbor

        draw_tile()

    return False

def display(position, value):
    font = pygame.font.SysFont('arial', 8)
    text = font.render(str(value), True, (0, 0, 0))
    WIN.blit(text, position)
    pygame.display.update()

def main(win, screen_width, screen_height):
    TOTAL_ROWS = 30
    TOTAL_COLS = 30
    grid = make_grid(TOTAL_ROWS, TOTAL_COLS, SCREEN_WIDTH, SCREEN_HEIGHT)

    start = None
    end = None

    running = True
    started = False

    increase_size = False

    while running:
        draw_tile(WIN, grid, TOTAL_ROWS, TOTAL_COLS, SCREEN_WIDTH, SCREEN_HEIGHT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]: # Left mouse button
                #Get position of mouse cursor
                pos = pygame.mouse.get_pos()
                row, col = get_click_pos(pos, TOTAL_COLS, SCREEN_WIDTH)
                tile = grid[row][col]
                # print(tile.step_cost)
                if not start and tile != end and tile.is_white():
                    start = tile
                    start.make_start()
                elif not end and tile != start and tile.is_white():
                    end = tile
                    end.make_end()
                elif tile != start and tile != end and not increase_size:
                    tile.make_barrier()
                elif tile != start and tile != end and increase_size:
                    tile.make_increase_size()
                    # print(grid[row][col].step_cost)




            elif pygame.mouse.get_pressed()[2]: #Right mouse button
                # Get position of mouse cursor
                pos = pygame.mouse.get_pos()
                row, col = get_click_pos(pos, TOTAL_COLS, SCREEN_WIDTH)
                tile = grid[row][col]
                tile.reset()
                if tile == start:
                    start = None
                elif tile == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end: #Make sure has start and end tile
                    for i in range(TOTAL_ROWS):
                        for j in range(TOTAL_COLS):
                            grid[i][j].update_neighbors(grid)
                    A_Star_Algorithm(lambda: draw_tile(WIN, grid, TOTAL_ROWS, TOTAL_COLS, SCREEN_WIDTH, SCREEN_HEIGHT),
                                     grid, start, end)

                elif event.key == pygame.K_1 and start and end:
                    increase_size = True
                elif event.key == pygame.K_2 and start and end:
                    increase_size = False


    pygame.quit()


main(WIN, SCREEN_WIDTH, SCREEN_HEIGHT)
