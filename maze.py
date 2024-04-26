import pygame
from variables import *
from cell import Cell
from block import Block

class Maze(Cell):
    """Class representing a maze made up of blocks of cells."""
    
    def __init__(self, x, y, block_in_maze, cell_size, line_width):
        """
        Initialize a maze.

        Args:
            x (int): The x-coordinate of the top-left corner of the maze.
            y (int): The y-coordinate of the top-left corner of the maze.
            block_in_maze (int): The number of blocks in each row and column of the maze.
            cell_size (int): The size of each cell in the maze.
            line_width (int): The width of the lines to draw for the maze.
        """
        self.x = x
        self.y = y
        self.block_in_maze = block_in_maze
        self.cell_size = cell_size
        self.line_width = line_width
        # Create a 2D array to hold blocks in the maze
        self.block = [[Block(x+j*cell_size*CELL_IN_BLOCK, y+i*cell_size*CELL_IN_BLOCK, i*block_in_maze+j, cell_size, line_width) for j in range(block_in_maze)] for i in range(block_in_maze)]
        
    def __str__(self):
        """
        Return a string representation of the maze.

        Returns:
            str: String representation of the maze.
        """
        maze_str = ""
        for i in range(self.block_in_maze):
            for j in range(self.block_in_maze):
                maze_str += str(self.block[i][j]) + '\n'  
        return maze_str
    
    def show_block_number(self):
        """
        Display the block numbers in the maze.

        Prints:
            str: The block numbers in the maze.
        """
        maze_str = ""
        for i in range(self.block_in_maze):
            for j in range(self.block_in_maze):
                maze_str += self.block[i][j].show_block_number() + ' '  
            maze_str += '\n'
        print(maze_str)
        
    def get_block_number_list(self):
        """
        Get a 2D list of block numbers in the maze.

        Returns:
            list: A 2D list of block numbers.
        """
        block_list = []
        for i in range(self.block_in_maze):
            row_block_list = []
            for j in range(self.block_in_maze):
                row_block_list.append(self.block[i][j].block_num)
            block_list.append(row_block_list)
        return block_list
    
    def get_block_number_index(self, block_number):
        """
        Get the row and column indices of a block with a given block number.

        Args:
            block_number (int): The number of the block.

        Returns:
            tuple: The row and column indices of the block.
        """
        for row in range(self.block_in_maze):
            for col in range(self.block_in_maze):
                if self.block[row][col].block_num == block_number:
                    return (row, col)
        print("Incorrect block number")
        return (-1, -1)
        
    def draw(self, window, color):
        """
        Draw the maze on the window.

        Args:
            window: The Pygame window surface to draw on.
            color: The color of the lines to draw.
        """
        for i in range(self.block_in_maze):
            for j in range(self.block_in_maze):
                self.block[i][j].draw(window, color)
                
    def move(self, dx, dy):
        """
        Move the maze and its blocks by the specified amount.

        Args:
            dx (int): The amount to move in the x-direction.
            dy (int): The amount to move in the y-direction.
        """
        self.x += dx
        self.y += dy
        for row in self.block:
            for block in row:
                block.move(dx, dy)
    
    def reset_pos(self):
        '''
        Resets the positions of the maze.
        '''
        self.x = 0
        self.y = 0
        for row in range(self.block_in_maze):
            for col in range(self.block_in_maze):
                self.block[row][col].reset_pos(col * self.cell_size * CELL_IN_BLOCK, row * self.cell_size * CELL_IN_BLOCK)
                
    def wrap_around(self, pos, direction):
        """
        Get the new position for pos + direction and wrap the new position around the maze 
        if it goes out of bounds.

        Args:
            pos (tuple): The current position (block_x, block_y, cell_x, cell_y).
            direction (tuple): The direction to move in (dir_x, dir_y).

        Returns:
            tuple: The wrapped position.
        """
        block_x, block_y, cell_x, cell_y = pos
        dir_x, dir_y = direction
        cell_x += dir_x
        cell_y += dir_y
        curr_pos = [block_x, block_y, cell_x, cell_y]
        
        # Indices for block and cell positions in the tuple
        cell_idx = 2
        for idx in [cell_idx,cell_idx+1]:
            if curr_pos[idx] < 0:
                # Wrap around to the opposite side of the maze
                curr_pos[idx] = CELL_IN_BLOCK - 1
                curr_pos[idx-2] -= 1
                if curr_pos[idx-2] < 0:
                    curr_pos[idx-2] = self.block_in_maze - 1
            if curr_pos[idx] >= CELL_IN_BLOCK:
                # Wrap around to the opposite side of the maze
                curr_pos[idx] = 0
                curr_pos[idx-2] += 1
                if curr_pos[idx-2] >= self.block_in_maze:
                    curr_pos[idx-2] = 0
        return tuple(curr_pos)            
                
    def generate_maze(self, my_seed):
        """
        Generate a maze within the Maze object using a depth-first search algorithm.

        Args:
            my_seed (int): Seed value for random number generation.

        Returns:
            list: The longest path found during maze generation.
        """
        random.seed(my_seed)
        
        # Create a copy of the DIRECTION list to avoid changing the original list
        direction_list = DIRECTION.copy()
        
        # Define a dictionary to map directions to their opposites
        direction_dict = {
            UP: DOWN,
            DOWN: UP,
            RIGHT: LEFT,
            LEFT: RIGHT
        }
        
        # Initialize sets and lists for tracking visited positions, the stack, and the longest path found
        visited = set()
        stack = []
        longest_path = []
        
        # Choose a random starting position within the maze
        start = (random.choice(range(self.block_in_maze)),random.choice(range(self.block_in_maze)),random.choice(range(CELL_IN_BLOCK)),random.choice(range(CELL_IN_BLOCK)))
        
        # Mark the starting position as visited
        visited.add(start)
        
        # Choose a random starting direction
        start_direction = random.choice(direction_list)
        # print(start, start_direction)
        
        # Push the starting position, direction, and path onto the stack
        stack.append((start, start_direction, [start, self.wrap_around(start, start_direction)]))
        
        # Main loop for maze generation
        while len(stack) > 0:
            # Pop the top element from the stack
            (pos, direction, path) = stack.pop()
            
             # Calculate the position in the current direction
            curr_pos = self.wrap_around(pos, direction)
            
            # Update the longest path found if the current path is longer
            if len(path) > len(longest_path):
                longest_path = path.copy()
                
            # If the current position has not been visited
            if curr_pos not in visited:
                # Mark the current position as visited
                visited.add(curr_pos)
                
                # Add the direction to the connection list of both current cell (current pos) and original cell (pos)
                self.block[pos[0]][pos[1]].cell[pos[2]][pos[3]].connect.append(direction)
                self.block[curr_pos[0]][curr_pos[1]].cell[curr_pos[2]][curr_pos[3]].connect.append(direction_dict[direction])
            
            # Shuffle the direction list to explore in a random order
            random.shuffle(direction_list)
            
            # Explore neighbors in the current position
            for direction in direction_list:
                new_pos = self.wrap_around(curr_pos, direction)
                # If the neighbor has not been visited and is not already in the stack
                if (new_pos not in visited) and ((curr_pos, direction, path) not in stack):
                    # Add the neighbor position, direction, and new path to the stack
                    new_path = path + [new_pos]
                    stack.append((curr_pos, direction, new_path))
                    
        # Return the longest path found during maze generation
        return longest_path
    
    def exchange_block(self, block1_idx, block2_idx):
        """
        Exchange the positions and connections of two blocks in the maze.

        Args:
            block1_idx (tuple): Indices of the first block (row, column).
            block2_idx (tuple): Indices of the second block (row, column).
        """
        block1_x, block1_y = block1_idx
        block2_x, block2_y = block2_idx
        
        for i in range(CELL_IN_BLOCK):
            for j in range(CELL_IN_BLOCK):
                temp_connect = self.block[block1_x][block1_y].cell[i][j].connect.copy()
                self.block[block1_x][block1_y].cell[i][j].connect = self.block[block2_x][block2_y].cell[i][j].connect.copy()
                self.block[block2_x][block2_y].cell[i][j].connect = temp_connect
        
        self.block[block1_x][block1_y].block_num, self.block[block2_x][block2_y].block_num = self.block[block2_x][block2_y].block_num, self.block[block1_x][block1_y].block_num

    
    def randomize(self, my_seed):
        """
        Randomly exchange the positions and connections of blocks in the maze.

        Args:
            my_seed (int): Seed value for random number generation.
        """
        random.seed(my_seed)
        for _ in range(10):
            self.exchange_block((random.choice(range(self.block_in_maze)),random.choice(range(self.block_in_maze))), (random.choice(range(self.block_in_maze)),random.choice(range(self.block_in_maze))))

    def draw_sol_line(self, pos_1, pos_2, window):
        """
        Draw a line representing a solution path between two positions in the maze.

        Args:
            pos_1 (tuple): The first position (block_row, block_col, cell_row, cell_col).
            pos_2 (tuple): The second position (block_row, block_col, cell_row, cell_col).
            window: The Pygame window surface to draw on.
        """
        # Calculate center coordinates of cells in the blocks
        block_1_row, block_1_col, cell_1_row, cell_1_col = pos_1
        block_2_row, block_2_col, cell_2_row, cell_2_col = pos_2
        block_1_center_x = self.block[block_1_row][block_1_col].cell[cell_1_row][cell_1_col].x + self.cell_size/2
        block_1_center_y = self.block[block_1_row][block_1_col].cell[cell_1_row][cell_1_col].y + self.cell_size/2
        block_2_center_x = self.block[block_2_row][block_2_col].cell[cell_2_row][cell_2_col].x + self.cell_size/2
        block_2_center_y = self.block[block_2_row][block_2_col].cell[cell_2_row][cell_2_col].y + self.cell_size/2
        
        # Draw the line between the centers of the cells
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
        """
        Draw the solution path on the maze.

        Args:
            path (list): The solution path containing positions.
            window: The Pygame window surface to draw on.
        """
        for i in range(len(path)-1):
            self.draw_sol_line(path[i], path[i+1], window)