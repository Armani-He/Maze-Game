import pygame
# import random
from cell import Cell
from variables import *

class Block(Cell):
    """Class representing a block of cells in the grid."""
    
    def __init__(self, x, y, block_num, cell_size, line_width):
        """
        Initialize a block.

        Args:
            x (int): The x-coordinate of the top-left corner of the block.
            y (int): The y-coordinate of the top-left corner of the block.
            block_num (int): The number of the block.
            cell_size (int): The size of each cell in the block.
            line_width (int): The width of the lines to draw for the block.
        """
        self.x = x
        self.y = y
        self.block_num = block_num
        self.cell_size = cell_size
        # Create a 2D array to hold cells in the block
        self.cell = [[Cell(x+j*self.cell_size, y+i*self.cell_size, cell_size, line_width) for j in range(CELL_IN_BLOCK)] for i in range(CELL_IN_BLOCK)]
      
    def __str__(self):
        """
        Return a string representation of the block.

        Returns:
            str: String representation of the block.
        """
        block_str = ""
        for i in range(CELL_IN_BLOCK):
            for j in range(CELL_IN_BLOCK):
                block_str += str(self.cell[i][j]) + " " + str(self.block_num) + '\n'  
        return block_str
    
    def show_block_number(self):
        """
        Get the block number as a string.

        Returns:
            str: The block number.
        """
        return str(self.block_num)
        
    def draw(self, window, color):
        """
        Draw the block and its cells on the window.

        Args:
            window: The Pygame window surface to draw on.
            color: The color of the lines to draw.
        """
        # Draw the block outline
        pygame.draw.rect(window, (128,128,128), (self.x, self.y, self.cell_size * CELL_IN_BLOCK, self.cell_size * CELL_IN_BLOCK), width=1)
        # Draw the cells in the block
        for i in range(CELL_IN_BLOCK):
            for j in range(CELL_IN_BLOCK):
                self.cell[i][j].draw(window, color)
        
    def move(self, dx, dy):
        """
        Move the block and its cells by the specified amount.

        Args:
            dx (int): The amount to move in the x-direction.
            dy (int): The amount to move in the y-direction.
        """
        self.x += dx
        self.y += dy
        # Move each cell in the block
        for row in self.cell:
            for cell in row:
                cell.x += dx
                cell.y += dy
                
    def reset_pos(self, x, y):
        '''
        Resets the positions of the block and its cells to the specified position.

        Args:
            x (int): The x-coordinate of the top-left corner of the block.
            y (int): The y-coordinate of the top-left corner of the block.
        '''
        self.x = x
        self.y = y
        # Reset the position of each cell in the block
        for row in range(CELL_IN_BLOCK):
            for col in range(CELL_IN_BLOCK):
                self.cell[row][col].x = x + col * self.cell_size
                self.cell[row][col].y = y + row * self.cell_size
