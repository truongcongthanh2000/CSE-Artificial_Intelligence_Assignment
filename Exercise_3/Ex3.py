import numpy as np
import random
import time
import pygame
import math
import enum
import queue

#______________________________________________PROGRAM MANUAL______________________________________________
#   Maze size is fixed at 32x32, this can be changed in the source code
#   Color:
#       - Wall: Black
#       - Empty: White
#       - Starting node: Red
#       - Ending node: Green
#   Controls:
#       - SPACEBAR to regen maze. Note this will also reset starting and ending node
#       - E to clear maze (gen a blank one)
#       - Q to switch between:
#           + EditMode.GRID to add or remove wall
#           + EditMode.START to move starting node
#           + EditMode.END to move ending node
#       - Left click on node to edit maze based on EditMode
#       - A to run A* algorithm from starting node to ending node


TILE_EMPTY = 0
TILE_WALL = math.inf

COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)
COLOR_GREY = (133, 133, 133)
COLOR_RED = (252, 73, 73)
COLOR_GREEN = (0,255,0)
COLOR_YELLOW = (240, 255, 79)
COLOR_LIGHT_YEL = (243, 255, 117)

class EditMode(enum.Enum):
    NONE = 0
    GRID = 1
    START = 2
    END = 3


class Maze:
    def __init__(self,row,col):
        self.height = row
        self.width = col

    def rand_recursive(self, top, bottom, left,right):
        start_range = bottom + 2
        end_range = top -1
        y = random.randrange(start_range,end_range,2)

        for column in range(left +1,right):
            self.maze[y][column] = TILE_WALL
        
        start_range = left + 2
        end_range = right -1 
        x= random.randrange(start_range,end_range,2)

        for row in range(bottom +1, top):
            self.maze[row][x] = TILE_WALL
        
        wall = random.randrange(4)
        holes = random.randrange(1,3)
        if wall != 0:
            for i in range(holes):
                gap = random.randrange(left+1,x,1)
                self.maze[y][gap] = TILE_EMPTY
        if wall != 1:
            for i in range(holes):
                gap = random.randrange(x + 1, right, 1)
                self.maze[y][gap] = TILE_EMPTY

        if wall != 2:
            for i in range(holes):
                gap = random.randrange(bottom + 1, y, 1)
                self.maze[gap][x] = TILE_EMPTY

        if wall != 3:
            for i in range(holes):
                gap = random.randrange(y + 1, top, 1)
                self.maze[gap][x] = TILE_EMPTY
        if top > y + 3 and x > left + 3:
            self.rand_recursive(top, y, left, x)

        if top > y + 3 and x + 3 < right:
            self.rand_recursive(top, y, x, right)

        if bottom + 3 < y and x + 3 < right:
            self.rand_recursive(y, bottom, x, right)

        if bottom + 3 < y and x > left + 3:
            self.rand_recursive(y, bottom, left, x)
            
    def rerand(self):
        self.maze = np.zeros((self.height,self.width))
        self.gen_wall()
        self.rand_recursive(self.height-1, 0, 0, self.width -1)

    def blank(self):
        self.maze = np.zeros((self.height,self.width))

    def gen_wall(self):
        for row in range(self.height):
            self.maze[row][0] = TILE_WALL
            self.maze[row][self.width-1] = TILE_WALL
        for col in range(self.width):
            self.maze[0][col] = TILE_WALL
            self.maze[self.height-1][col] = TILE_WALL
    
    def get_neighbors(self,current):
        neighbors = []
        for row in range(current[0] -1,current[0] +2):
            for col in range (current[1] -1, current[1] +2):
                if (row >=0 and row < self.height and col >=0 and col < self.width):
                    if self.maze[row][col] == TILE_EMPTY and (row,col) != current:
                        neighbors.append((row,col))
        return neighbors

def h_x(goal,next):
    return math.sqrt(math.pow(goal[0] - next[0], 2) + math.pow(goal[1]-next[1], 2))

class App:
    windowWidth = 720
    windowHeight = 720
    start = None
    end = None
    path = []
    path_screen = []


    def __init__(self):
        self._running = True
        self.maze = Maze(33,33)
        self.maze.rerand()
        self._rect_size = math.floor(min(self.windowHeight,self.windowWidth)/max(self.maze.width,self.maze.height)) -1
        self._rects = []
        self.draw_rects()
        self.editmode = EditMode.NONE

    def draw_rects(self):
        self._rects = []
        for x in range(self.maze.height):
            for y in range(self.maze.width):
                rect = pygame.Rect(x*(self._rect_size +1), y*(self._rect_size +1), self._rect_size, self._rect_size)
                color =  COLOR_WHITE if self.maze.maze[x][y] == TILE_EMPTY else COLOR_BLACK
                self._rects.append((rect,color))

    def draw_path(self):
        self.path_screen = list(map(lambda x: ((x[0])*(self._rect_size +1) + round(self._rect_size/2),(x[1])*(self._rect_size +1)+ round(self._rect_size/2)),self.path))
        #print(self.path_screen)
    
    def edit_rects(self,pos,color_new):
        #print("Editing")
        for index,(rect,color) in enumerate(self._rects):
            if index == pos[0]*self.maze.height + pos[1]:
                self._rects[index] = (rect,color_new)
                #print("Switching " + str(pos) + " from color " + str(color) + " to color " + str(color_new))
    
    def edit_maze(self):
        pos = pygame.mouse.get_pos()
        col = pos[1] // (self._rect_size + 1)
        row = pos[0] // (self._rect_size + 1)
        self.maze.maze[row][col] = TILE_EMPTY if self.maze.maze[row][col] == TILE_WALL else TILE_WALL
        self.edit_rects((row,col), COLOR_WHITE if self.maze.maze[row][col] == TILE_EMPTY else COLOR_BLACK)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight),pygame.HWSURFACE)
        pygame.display.set_caption('Maze A*')
        self._running = True

    def on_event(self,event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.maze.rerand()
                self.draw_rects()
                self.start = None
                self.end = None
            if event.key == pygame.K_q:
                self.toggle_mode()
            if event.key == pygame.K_a:
                if self.start is not None and self.end is not None:
                    self.path = self.A_Star(self.start,self.end)
                    self.draw_path()
            if event.key == pygame.K_e:
                self.maze.blank()
                self.start = None
                self.end = None
                self.path = []
                self.draw_rects()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.editmode == EditMode.GRID:
                self.edit_maze()
            if self.editmode == EditMode.START:
                self.start = self.mark_point(self.start, COLOR_RED)
            if self.editmode == EditMode.END:
                self.end = self.mark_point(self.end, COLOR_GREEN)

    def on_loop(self):
        pygame.event.pump()
        events = pygame.event.get()

        for event in events:
            self.on_event(event)

    def on_render(self):
        self._display_surf.fill(COLOR_GREY)
        for rect,color in self._rects:
            pygame.draw.rect(self._display_surf, color, rect)
        if (self.path != []):
            pygame.draw.lines(self._display_surf, COLOR_BLACK, False, self.path_screen)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
        exit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        while (self._running):
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def toggle_mode(self):
        if  self.editmode == EditMode.GRID:
            self.editmode = EditMode.START
        elif self.editmode == EditMode.START:
            self.editmode = EditMode.END
        elif self.editmode == EditMode.END:
            self.editmode = EditMode.NONE
        elif self.editmode == EditMode.NONE:
            self.editmode = EditMode.GRID
        print("Current mode: ",end="")
        print(self.editmode)

    def mark_point(self,reg,color):
        #print(reg)
        if reg is not None:
            #print("Reg is not None")
            self.edit_rects(reg, COLOR_WHITE)
            reg = None
        pos = pygame.mouse.get_pos()
        col = pos[1] // (self._rect_size + 1)
        row = pos[0] // (self._rect_size + 1)
        if self.maze.maze[row][col] == TILE_EMPTY:
            reg = (row,col)
            #print(reg)
            self.edit_rects(reg, color)
        return reg

    def A_Star(self,start,goal):
        graph = self.maze
        frontier = queue.PriorityQueue()
        frontier.put(start,0)
        came_from = dict()
        cost_so_far = dict()
        came_from[start] = None
        cost_so_far[start] = 0
        path = []

        self.freeze = True

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                while current is not None:
                    #print(current)
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path
            for next in graph.get_neighbors(current):
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + h_x(goal,next)
                    frontier.put(next,priority)
                    came_from[next] = current

        return []
        

if __name__ == "__main__" :
    random.seed(time.time())
    newApp = App()
    newApp.on_execute()