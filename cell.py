import pygame
from variables import LEFT, RIGHT, UP, DOWN

class Cell:
    """Class representing a cell in the grid."""
    
    def __init__(self, x, y, cell_size, line_width) -> None:
        """
        Initialize a cell.

        Args:
            x (int): The x-coordinate of the top-left corner of the cell.
            y (int): The y-coordinate of the top-left corner of the cell.
            cell_size (int): The size of the cell.
            line_width (int): The width of the lines to draw for the cell.
        """
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.line_width = line_width
        self.connect = []
        
    def __str__(self):
        """
        Return a string representation of the cell.

        Returns:
            str: String representation of the cell.
        """
        return f'x:{self.x} y:{self.y} connect: {self.connect}'
    
    def draw(self, window, color):
        """
        Draw the maze wall on the window.

        Args:
            window: The Pygame window surface to draw on.
            color: The color of the lines to draw.
        """
        if LEFT not in self.connect:
            pygame.draw.line(window, color, (self.x, self.y), (self.x, self.y + 1 * self.cell_size), self.line_width)
        if UP not in self.connect:
            pygame.draw.line(window, color, (self.x, self.y), (self.x + 1 * self.cell_size, self.y), self.line_width)
        if RIGHT not in self.connect:
            pygame.draw.line(window, color, (self.x + 1 * self.cell_size, self.y), (self.x + 1 * self.cell_size, self.y + 1 * self.cell_size), self.line_width)
        if DOWN not in self.connect:
            pygame.draw.line(window, color, (self.x , self.y + 1 * self.cell_size), (self.x + 1 * self.cell_size, self.y + 1 * self.cell_size), self.line_width)                         
