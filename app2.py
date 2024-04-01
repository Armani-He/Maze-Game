import pygame
import random
import time


SCREEN_WIDTH = 900
SCREEN_HEIGHT = 840
VISIBLE_WIDTH = 720
VISIBLE_HEIGHT = 720
CELL_SIZE = 20
CELL_IN_BLOCK = 8
BLOCK_IN_MAZE = 2
BLOCK_SIZE = CELL_IN_BLOCK * CELL_SIZE
MAZE_SIZE = BLOCK_IN_MAZE * BLOCK_SIZE
# LEFT, RIGHT, UP, DOWN = (-1,0), (1,0), (0,-1), (0,1)
LEFT, RIGHT, UP, DOWN = (0,-1), (0,1), (-1,0), (1,0)
DIRECTION = [LEFT, RIGHT, UP, DOWN]
WHITE = (255,255,255)
RED = (255, 0, 0)
seed = random.randint(0, 1000)
# seed=42
random.seed(seed)

class Cell:
    def __init__(self, x, y, cell_size, line_width) -> None:
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.line_width = line_width
        self.connect = []
        
    def __str__(self):
        return f'x:{self.x} y:{self.y} connect: {self.connect}'
    
    def draw(self, window):
        # print(self.connect)
        if LEFT not in self.connect:
            # print("LEFT WALL")
            pygame.draw.line(window, (0,0,255), (self.x, self.y), (self.x, self.y + 1 * self.cell_size), self.line_width)
        if UP not in self.connect:
            # print("UP WALL")
            pygame.draw.line(window, (0,0,255), (self.x, self.y), (self.x + 1 * self.cell_size, self.y), self.line_width)
        if RIGHT not in self.connect:
            # print("RIGHT WALL")
            pygame.draw.line(window, (0,0,255), (self.x + 1 * self.cell_size, self.y), (self.x + 1 * self.cell_size, self.y + 1 * self.cell_size), self.line_width)
        if DOWN not in self.connect:
            # print("DOWN WALL")
            pygame.draw.line(window, (0,0,255), (self.x , self.y + 1 * self.cell_size), (self.x + 1 * self.cell_size, self.y + 1 * self.cell_size), self.line_width)                         
            # print(time.sleep(1))
            # pygame.display.update()

class Block(Cell):
    def __init__(self, x, y, block_num, cell_size, line_width):
        self.x = x
        self.y = y
        self.block_num = block_num
        self.cell_size = cell_size
        self.cell = [[Cell(x+j*self.cell_size, y+i*self.cell_size, cell_size, line_width) for j in range(CELL_IN_BLOCK)] for i in range(CELL_IN_BLOCK)]
      
    def __str__(self):
        block_str = ""
        for i in range(CELL_IN_BLOCK):
            for j in range(CELL_IN_BLOCK):
                block_str += str(self.cell[i][j]) + " " + str(self.block_num) + '\n'  
        return block_str
    
    def show_block_number(self):
        return str(self.block_num)
        
    def draw(self, window):
        pygame.draw.rect(window, (128,128,128), (self.x, self.y, self.cell_size * CELL_IN_BLOCK, self.cell_size * CELL_IN_BLOCK), width=1)
        for i in range(CELL_IN_BLOCK):
            for j in range(CELL_IN_BLOCK):
                self.cell[i][j].draw(window)
        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        for row in self.cell:
            for cell in row:
                cell.x += dx
                cell.y += dy
    
    def wrap_around(self, pos, direction):
        curr_pos = [p + d for p, d in zip(pos, direction)]
        for idx in [0,1]:
            if curr_pos[idx] < 0:
                curr_pos[idx] = CELL_IN_BLOCK - 1
            if curr_pos[idx] >= CELL_IN_BLOCK:
                curr_pos[idx] = 0
        return tuple(curr_pos)
                
    def generate_maze(self):
        direction_dict = {
            UP: DOWN,
            DOWN: UP,
            RIGHT: LEFT,
            LEFT: RIGHT
        }
        visited = []
        stack = []
        start = (random.choice(range(CELL_IN_BLOCK)),random.choice(range(CELL_IN_BLOCK)))
        visited.append(start)
        stack.append((start, random.choice(DIRECTION)))
        while len(stack) > 0:
            print(visited)
            (pos, direction) = stack.pop()
            curr_pos = self.wrap_around(pos, direction)
            if curr_pos not in visited:
                visited.append(curr_pos)
                self.cell[pos[0]][pos[1]].connect.append(direction)
                self.cell[curr_pos[0]][curr_pos[1]].connect.append(direction_dict[direction])
            random.shuffle(DIRECTION)
            for direction in DIRECTION:
                new_pos = self.wrap_around(curr_pos, direction)
                if (new_pos not in visited) and ((curr_pos, direction) not in stack):
                    stack.append((curr_pos, direction))
        return start
        
class Maze(Cell):
    def __init__(self, x, y, block_in_maze, cell_size, line_width):
        self.x = x
        self.y = y
        self.block_in_maze = block_in_maze
        self.cell_size = cell_size
        self.line_width = line_width
        self.block = [[Block(x+j*cell_size*CELL_IN_BLOCK, y+i*cell_size*CELL_IN_BLOCK, i*block_in_maze+j, cell_size, line_width) for j in range(block_in_maze)] for i in range(block_in_maze)]
        
    def __str__(self):
        maze_str = ""
        for i in range(self.block_in_maze):
            for j in range(self.block_in_maze):
                maze_str += str(self.block[i][j]) + '\n'  
        return maze_str
    
    def show_block_number(self):
        maze_str = ""
        for i in range(self.block_in_maze):
            for j in range(self.block_in_maze):
                maze_str += self.block[i][j].show_block_number() + ' '  
            maze_str += '\n'
        print(maze_str)
        
    def draw(self, window):
        for i in range(self.block_in_maze):
            for j in range(self.block_in_maze):
                self.block[i][j].draw(window)
                
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        for row in self.block:
            for block in row:
                block.move(dx, dy)
                
    def wrap_around(self, pos, direction):
        block_x, block_y, cell_x, cell_y = pos
        dir_x, dir_y = direction
        cell_x += dir_x
        cell_y += dir_y
        curr_pos = [block_x, block_y, cell_x, cell_y]
        
        block_idx = 0
        cell_idx = 2
        for idx in [cell_idx,cell_idx+1]:
            if curr_pos[idx] < 0:
                curr_pos[idx] = CELL_IN_BLOCK - 1
                curr_pos[idx-2] -= 1
                if curr_pos[idx-2] < 0:
                    curr_pos[idx-2] = self.block_in_maze - 1
            if curr_pos[idx] >= CELL_IN_BLOCK:
                curr_pos[idx] = 0
                curr_pos[idx-2] += 1
                if curr_pos[idx-2] >= self.block_in_maze:
                    curr_pos[idx-2] = 0
        return tuple(curr_pos)            
                
    def generate_maze(self, seed):
        random.seed(seed)
        direction_list = DIRECTION.copy()
        direction_dict = {
            UP: DOWN,
            DOWN: UP,
            RIGHT: LEFT,
            LEFT: RIGHT
        }
        visited = set()
        stack = []
        longest_path = []
        start = (random.choice(range(self.block_in_maze)),random.choice(range(self.block_in_maze)),random.choice(range(CELL_IN_BLOCK)),random.choice(range(CELL_IN_BLOCK)))
        
        # start = (0, 0, 0, 0)
        visited.add(start)
        start_direction = random.choice(direction_list)
        print(start, start_direction)
        stack.append((start, start_direction, [start, self.wrap_around(start, start_direction)]))
        while len(stack) > 0:
            # print(visited)
            # print(str(maze))
            (pos, direction, path) = stack.pop()
            curr_pos = self.wrap_around(pos, direction)
            if len(path) > len(longest_path):
                longest_path = path.copy()
            if curr_pos not in visited:
                visited.add(curr_pos)
                self.block[pos[0]][pos[1]].cell[pos[2]][pos[3]].connect.append(direction)
                self.block[curr_pos[0]][curr_pos[1]].cell[curr_pos[2]][curr_pos[3]].connect.append(direction_dict[direction])
            random.shuffle(direction_list)
            for direction in direction_list:
                new_pos = self.wrap_around(curr_pos, direction)
                if (new_pos not in visited) and ((curr_pos, direction, path) not in stack):
                    new_path = path + [new_pos]
                    stack.append((curr_pos, direction, new_path))
        return longest_path
    
    def exchange_block(self, block1_idx, block2_idx):
        block1_x, block1_y = block1_idx
        block2_x, block2_y = block2_idx
        
        for i in range(CELL_IN_BLOCK):
            for j in range(CELL_IN_BLOCK):
                temp_connect = self.block[block1_x][block1_y].cell[i][j].connect.copy()
                self.block[block1_x][block1_y].cell[i][j].connect = self.block[block2_x][block2_y].cell[i][j].connect.copy()
                self.block[block2_x][block2_y].cell[i][j].connect = temp_connect
        
        self.block[block1_x][block1_y].block_num, self.block[block2_x][block2_y].block_num = self.block[block2_x][block2_y].block_num, self.block[block1_x][block1_y].block_num

    def find_longest_path(self, start):
        longest_path = []
        stack = [(start, [start])]
        visited = set()

        while stack:
            pos, path = stack.pop()
            visited.add(pos)

            neighbors = [self.wrap_around(pos, direction) for direction in DIRECTION]
            for new_pos in neighbors:
                if new_pos not in visited:
                    new_path = path + [new_pos]
                    stack.append((new_pos, new_path))
                    if len(new_path) > len(longest_path):
                        longest_path = new_path

        return longest_path
    
    def randomize(self, seed):
        random.seed(seed)
        for _ in range(10):
            self.exchange_block((random.choice(range(self.block_in_maze)),random.choice(range(self.block_in_maze))), (random.choice(range(self.block_in_maze)),random.choice(range(self.block_in_maze))))

    def draw_sol_line(self, pos_1, pos_2, window):
        block_1_row, block_1_col, cell_1_row, cell_1_col = pos_1
        block_2_row, block_2_col, cell_2_row, cell_2_col = pos_2
        block_1_center_x = self.block[block_1_row][block_1_col].cell[cell_1_row][cell_1_col].x + self.cell_size/2
        block_1_center_y = self.block[block_1_row][block_1_col].cell[cell_1_row][cell_1_col].y + self.cell_size/2
        block_2_center_x = self.block[block_2_row][block_2_col].cell[cell_2_row][cell_2_col].x + self.cell_size/2
        block_2_center_y = self.block[block_2_row][block_2_col].cell[cell_2_row][cell_2_col].y + self.cell_size/2
        # block in maze must > 2
        if block_2_row - block_1_row in [0, 1, -1] and block_2_col - block_1_col in [0, 1, -1]:
            pygame.draw.line(window, RED, (block_1_center_x, block_1_center_y), (block_2_center_x, block_2_center_y), self.line_width)
        # block_1 + UP -> block_2
        elif block_2_row > block_1_row:
            pygame.draw.line(window, RED, (block_1_center_x, block_1_center_y), (block_1_center_x, block_1_center_y - self.cell_size/2), self.line_width)
            pygame.draw.line(window, RED, (block_2_center_x, block_2_center_y), (block_2_center_x, block_2_center_y + self.cell_size/2), self.line_width)
        # block_1 + DOWN -> block_2
        elif block_2_row < block_1_row:
            pygame.draw.line(window, RED, (block_1_center_x, block_1_center_y), (block_1_center_x, block_1_center_y + self.cell_size/2), self.line_width)
            pygame.draw.line(window, RED, (block_2_center_x, block_2_center_y), (block_2_center_x, block_2_center_y - self.cell_size/2), self.line_width)
        # block_1 + LEFT -> block_2
        elif block_2_col > block_1_col:
            pygame.draw.line(window, RED, (block_1_center_x, block_1_center_y), (block_1_center_x - self.cell_size/2, block_1_center_y), self.line_width)
            pygame.draw.line(window, RED, (block_2_center_x, block_2_center_y), (block_2_center_x + self.cell_size/2, block_2_center_y), self.line_width)
        # block_1 + RIGHT -> block_2
        elif block_2_col < block_1_col:
            pygame.draw.line(window, RED, (block_1_center_x, block_1_center_y), (block_1_center_x + self.cell_size/2, block_1_center_y), self.line_width)
            pygame.draw.line(window, RED, (block_2_center_x, block_2_center_y), (block_2_center_x - self.cell_size/2, block_2_center_y), self.line_width)
  
            
    def draw_sol(self, path, window):
        for i in range(len(path)-1):
            self.draw_sol_line(path[i], path[i+1], window)


def save_image(maze, find_sol, file_name):
    output_maze_surface = pygame.Surface((maze.block_in_maze*CELL_IN_BLOCK*maze.cell_size, maze.block_in_maze*CELL_IN_BLOCK*maze.cell_size))
    output_maze_surface.fill(WHITE)
    maze.draw(output_maze_surface)
    if find_sol is True:
        maze.draw_sol(solution_path, output_maze_surface)
    pygame.image.save(output_maze_surface, file_name)

pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
window.fill(WHITE)
maze_surface = pygame.Surface((VISIBLE_WIDTH, VISIBLE_HEIGHT))
maze_surface.set_alpha(128)
small_maze_surface = pygame.Surface((SCREEN_WIDTH-VISIBLE_WIDTH,SCREEN_WIDTH-VISIBLE_WIDTH))
# cell = Cell(20,20)
# cell.draw()
# block = Block(0,0,0, 30, 3)
# block.generate_maze()
# print(str(block))
# block.draw(window)
maze = Maze(0, 0, 3, 90, 10)
small_maze = Maze(0, 0, 3, 10, 3)
pygame.display.update()

solution_path = maze.generate_maze(seed)
small_maze.generate_maze(seed)
maze.show_block_number()
with open("path.txt", "w") as fh:
    fh.write("block_row, block_col, cell_row, cell_col\n")
    for pos in solution_path:
        fh.write(str(pos)+'\n')
# print(solution_path)
save_image(maze, True, "solution.jpg")

window.fill(WHITE)
maze_surface.fill(WHITE)
maze.draw(maze_surface)
window.blit(maze_surface, (0,0))
pygame.display.update()

# print(f'old maze: {str(maze.block[0][0])}')
# print(f'old maze2: {str(small_maze.block[0][0])}')

time.sleep(3)
# maze.exchange_block((0,1),(1,0))
maze.randomize(seed)
save_image(maze, False, "maze.jpg")
small_maze.randomize(seed)
save_image(small_maze, False, "maze2.jpg")

# pygame.draw.rect(window, WHITE, pygame.Rect(maze.block[0][1].x, maze.block[0][1].y, BLOCK_SIZE, BLOCK_SIZE))
# pygame.draw.rect(window, WHITE, pygame.Rect(maze.block[1][0].x, maze.block[1][0].y, BLOCK_SIZE, BLOCK_SIZE))
# maze.block[0][1].draw()
# maze.block[1][0].draw()

window.fill(WHITE)
maze_surface.fill(WHITE)
small_maze_surface.fill(WHITE)
maze.draw(maze_surface)
small_maze.draw(small_maze_surface)
window.blit(maze_surface, (0,0))
window.blit(small_maze_surface, (VISIBLE_WIDTH+5,0))
maze.show_block_number()
pygame.display.update()

for i in range(10):
    time.sleep(1)
    maze.move(-maze.cell_size, 0)
    maze_surface.fill(WHITE)
    maze.draw(maze_surface)
    window.blit(maze_surface, (0,0))
    pygame.display.update()

# print(f'New maze: {str(maze)}')

running = True

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False