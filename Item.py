from maze import Maze
from variables import *
class Item:
    def __init__(self, pos, block_in_maze, key):
        """
        Initialize an Item object with specified attributes.

        Args:
            pos (tuple): The position of the item (block_row, block_col, cell_row, cell_col).
            block_in_maze (int): The number of blocks in each row and column of the maze.
            key: The unique key of the item.
        """
        block_row, block_col, cell_row, cell_col = pos
        self.block_number = block_row * block_in_maze + block_col
        self.cell_row = cell_row
        self.cell_col = cell_col
        self.key = key
        self.collect = False
        self.visible = False
    
    def get_absolute_pos(self, maze:Maze):
        """
        Get the absolute position of the item within the maze.

        Args:
            maze (Maze): The Maze object containing the item.

        Returns:
            tuple: The absolute position (pos_x, pos_y) of the item.
        """
        block_size = maze.cell_size * CELL_IN_BLOCK
        block_row, block_col = maze.get_block_number_index(self.block_number)
        pos_x, pos_y = (block_col * block_size + self.cell_col * maze.cell_size, \
                        block_row * block_size + self.cell_row * maze.cell_size)
        return pos_x, pos_y
    
class Coin(Item):
    def __init__(self, pos, block_in_maze, key):
        """
        Initialize a Coin object, inheriting from Item.

        Args:
            pos (tuple): The position of the coin (block_row, block_col, cell_row, cell_col).
            block_in_maze (int): The number of blocks in the maze.
            key: The unique key of the coin.
        """
        super().__init__(pos, block_in_maze, key)
        self.visible = True
        
class Coke(Item):
    def __init__(self, pos, block_in_maze, key):
        super().__init__(pos, block_in_maze, key)

class Meat(Item):
    def __init__(self, pos, block_in_maze, key):
        super().__init__(pos, block_in_maze, key)

class Sword(Item):
    def __init__(self, pos, block_in_maze, key):
        super().__init__(pos, block_in_maze, key)

class Shield(Item):
    def __init__(self, pos, block_in_maze, key):
        super().__init__(pos, block_in_maze, key)

class FinishFlag(Item):
    def __init__(self, pos, block_in_maze, key):
        """
        Initialize a FinishFlag object, inheriting from Item.

        Args:
            pos (tuple): The position of the finish flag (block_row, block_col, cell_row, cell_col).
            block_in_maze (int): The number of blocks in the maze.
            key: The unique key of the finish flag.
        """
        super().__init__(pos, block_in_maze, key)
        self.visible = True