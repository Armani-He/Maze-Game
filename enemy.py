from dice import Dice
from maze import Maze
from variables import *

class Enemy:
    def __init__(self, name, life, attack, defense, attack_dice:Dice, defense_dice:Dice, pos, block_in_maze, image_path, key):
        """
        Initialize an Enemy object with specified attributes.

        Args:
            name (str): The name of the enemy.
            life (int): The initial life points of the enemy.
            attack (int): The attack power of the enemy.
            defense (int): The defense power of the enemy.
            attack_dice (Dice): A Dice object representing the attack dice of the enemy.
            defense_dice (Dice): A Dice object representing the defense dice of the enemy.
            pos (tuple): The position of the enemy (block_row, block_col, cell_row, cell_col).
            block_in_maze (int): The number of blocks in each row and column of the maze.
            image_path (str): The path to the image file of the enemy.
            key: The unique key of the enemy.
        """
        block_row, block_col, cell_row, cell_col = pos
        block_number = block_row * block_in_maze + block_col
        self.block_number = block_number
        self.name = name
        self.cell_row = cell_row
        self.cell_col = cell_col
        self.visible = False
        self.image_path = image_path
        self.life = life
        self.initial_life = life
        self.attack = attack
        self.initial_attack = attack
        self.defense = defense
        self.initial_defense = defense
        self.attack_dice = attack_dice
        self.defense_dice = defense_dice
        self.fame = life * 10 + (attack + defense) * 100 + (sum(range(attack_dice.lower_bound, attack_dice.upper_bound+1)) +\
                                                            sum(range(defense_dice.lower_bound, defense_dice.upper_bound+1))) * 200
        self.key = key
        self.defeated = False
    
    def get_absolute_pos(self, maze: Maze):
        """
        Get the absolute position of the enemy within the maze.

        Args:
            maze (Maze): The Maze object containing the enemy.

        Returns:
            tuple: The absolute position (pos_x, pos_y) of the enemy.
        """
        block_size = maze.cell_size * CELL_IN_BLOCK
        block_row, block_col = maze.get_block_number_index(self.block_number)
        pos_x, pos_y = (block_col * block_size + self.cell_col * maze.cell_size, \
                        block_row * block_size + self.cell_row * maze.cell_size)
        return pos_x, pos_y