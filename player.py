from maze import Maze
from variables import *
from dice import Dice

class Player():
    def __init__(self, pos, maze: Maze):
        """
        Initialize a Player object with specified attributes.

        Args:
            pos (tuple): The initial position of the player (block_row, block_col, cell_row, cell_col).
            maze (Maze): The Maze object in which the player exists.
        """
        (block_row, block_col, cell_row, cell_col) = pos
        self.block_number = block_row * maze.block_in_maze + block_col
        self.cell_row = cell_row
        self.cell_col = cell_col
        self.life = 150
        self.maximum_life = self.life
        self.attack = 5
        self.defense = 1
        self.coin = 50
        self.step = 0
        self.fame = 0
        self.attack_dice = Dice(1, 6)
        self.defense_dice = Dice(1, 6)
        self.lucky_gambling_dice_activate = False
            
    def move_right(self, maze: Maze):
        """
        Move the player to the right within the maze.

        Args:
            maze (Maze): The Maze object in which the player exists.
        """
        block_row, block_col = maze.get_block_number_index(self.block_number)
        if self.cell_col < CELL_IN_BLOCK - 1:
            self.cell_col += 1
            return
        elif self.cell_col == CELL_IN_BLOCK - 1 and block_col < maze.block_in_maze - 1:
            block_col += 1
            self.cell_col = 0
            self.block_number = maze.block[block_row][block_col].block_num
            return
        return
            
    def move_left(self, maze: Maze):
        """
        Move the player to the left within the maze.

        Args:
            maze (Maze): The Maze object in which the player exists.
        """
        block_row, block_col = maze.get_block_number_index(self.block_number)
        if self.cell_col > 0:
            self.cell_col -= 1
            return
        elif self.cell_col == 0 and block_col > 0:
            block_col -= 1
            self.cell_col = CELL_IN_BLOCK - 1
            self.block_number = maze.block[block_row][block_col].block_num
            return
        return
    
    def move_down(self, maze: Maze):
        """
        Move the player down within the maze.

        Args:
            maze (Maze): The Maze object in which the player exists.
        """
        block_row, block_col = maze.get_block_number_index(self.block_number)
        if self.cell_row < CELL_IN_BLOCK - 1:
            self.cell_row += 1
            return
        elif self.cell_row == CELL_IN_BLOCK - 1 and block_row < maze.block_in_maze - 1:
            block_row += 1
            self.cell_row = 0
            self.block_number = maze.block[block_row][block_col].block_num
            return
        return
    
    def move_up(self, maze: Maze):
        """
        Move the player up within the maze.

        Args:
            maze (Maze): The Maze object in which the player exists.
        """
        block_row, block_col = maze.get_block_number_index(self.block_number)
        if self.cell_row > 0:
            self.cell_row -= 1
            return
        elif self.cell_row == 0 and block_row > 0:
            block_row -= 1
            self.cell_row = CELL_IN_BLOCK - 1
            self.block_number = maze.block[block_row][block_col].block_num
            return
        return

    def get_absolute_pos(self, maze: Maze):
        """
        Get the absolute position (in pixels) of the player within the maze.

        Args:
            maze (Maze): The Maze object containing the player.

        Returns:
            tuple: The absolute position (pos_x, pos_y) of the player.
        """
        block_size = maze.cell_size * CELL_IN_BLOCK
        block_row, block_col = maze.get_block_number_index(self.block_number)
        pos_x, pos_y = (block_col * block_size + self.cell_col * maze.cell_size, \
                        block_row * block_size + self.cell_row * maze.cell_size)
        return pos_x, pos_y