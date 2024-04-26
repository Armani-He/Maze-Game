import pygame
import random
import time
from variables import *
from maze import Maze
from player import Player
from Item import Item, Coin, Sword, Meat, Coke, Shield, FinishFlag
from dice import Dice
from enemy import Enemy
from helper import Helper
import skill

def save_image(maze: Maze, find_sol, file_name, solution_path):
    """
    Save an image of the maze to a file.

    Args:
        maze (Maze): The Maze object representing the maze to be saved.
        find_sol (bool): Flag indicating whether a solution path is found.
        file_name (str): The name of the file to save the image.
        solution_path (list): The solution path to be drawn on the maze image.

    Returns:
        None
    """
    output_maze_surface = pygame.Surface((maze.block_in_maze*CELL_IN_BLOCK*maze.cell_size, maze.block_in_maze*CELL_IN_BLOCK*maze.cell_size))
    output_maze_surface.fill(WHITE)
    maze.draw(output_maze_surface, DARK_BROWN)
    if find_sol is True:
        maze.draw_sol(solution_path, output_maze_surface)
    pygame.image.save(output_maze_surface, file_name)
    
def show_maze_on_window(maze: Maze, window: pygame.Surface, surface: pygame.Surface, pos):
    """
    Draw the maze on a surface and then render it to the window at the specified position.

    Args:
        maze (Maze): The Maze object representing the maze to be drawn.
        window (pygame.Surface): The window surface where the maze will be rendered.
        surface (pygame.Surface): The surface to draw the maze on.
        pos (tuple): The position to render the maze on the window.

    Returns:
        None
    """
    
    if maze.cell_size == SMALL_MAZE_CELL_SIZE:
        surface.fill(DARK_BROWN)
        maze.draw(surface, LIGHT_BROWN)
    else:
        surface.fill(LIGHT_BROWN)
        maze.draw(surface, DARK_BROWN)
    # maze.draw(surface, LINE_COLOR)
    window.blit(surface, pos)
    
def check_up_validate(maze: Maze, player: Player):
    """
    Check if moving up from the player's current position is a valid move within the maze.

    Args:
        maze (Maze): The Maze object representing the maze.
        player (Player): The Player object representing the player.

    Returns:
        bool: True if moving up is valid, False otherwise.
    """
    block_row, block_col = maze.get_block_number_index(player.block_number)
    curr_pos = (block_row, block_col, player.cell_row, player.cell_col)
    if player.cell_row == 0 and block_row == 0:
        return False
    if player.cell_row > 0:
        up_pos = (block_row, block_col, player.cell_row - 1, player.cell_col)
    elif player.cell_row == 0 and block_row > 0:
        up_pos = (block_row - 1, block_col, CELL_IN_BLOCK - 1, player.cell_col)
    return UP in maze.block[curr_pos[0]][curr_pos[1]].cell[curr_pos[2]][curr_pos[3]].connect and \
           DOWN in maze.block[up_pos[0]][up_pos[1]].cell[up_pos[2]][up_pos[3]].connect
           
def check_down_validate(maze: Maze, player: Player):
    """
    Check if moving down from the player's current position is a valid move within the maze.

    Args:
        maze (Maze): The Maze object representing the maze.
        player (Player): The Player object representing the player.

    Returns:
        bool: True if moving down is valid, False otherwise.
    """
    block_row, block_col = maze.get_block_number_index(player.block_number)
    curr_pos = (block_row, block_col, player.cell_row, player.cell_col)
    if player.cell_row == CELL_IN_BLOCK - 1 and block_row == maze.block_in_maze - 1:
        return False
    if player.cell_row < CELL_IN_BLOCK - 1:
        down_pos = (block_row, block_col, player.cell_row + 1, player.cell_col)
    elif player.cell_row == CELL_IN_BLOCK - 1 and block_row < maze.block_in_maze - 1:
        down_pos = (block_row + 1, block_col, 0, player.cell_col)
    return DOWN in maze.block[curr_pos[0]][curr_pos[1]].cell[curr_pos[2]][curr_pos[3]].connect and \
           UP in maze.block[down_pos[0]][down_pos[1]].cell[down_pos[2]][down_pos[3]].connect
           
def check_left_validate(maze: Maze, player: Player):
    """
    Check if moving left from the player's current position is a valid move within the maze.

    Args:
        maze (Maze): The Maze object representing the maze.
        player (Player): The Player object representing the player.

    Returns:
        bool: True if moving left is valid, False otherwise.
    """
    block_row, block_col = maze.get_block_number_index(player.block_number)
    curr_pos = (block_row, block_col, player.cell_row, player.cell_col)
    if player.cell_col == 0 and block_col == 0:
        return False
    if player.cell_col > 0:
        left_pos = (block_row, block_col, player.cell_row, player.cell_col - 1)
    elif player.cell_col == 0 and block_col > 0:
        left_pos = (block_row, block_col - 1, player.cell_row, CELL_IN_BLOCK - 1)
    return LEFT in maze.block[curr_pos[0]][curr_pos[1]].cell[curr_pos[2]][curr_pos[3]].connect and \
           RIGHT in maze.block[left_pos[0]][left_pos[1]].cell[left_pos[2]][left_pos[3]].connect
           
def check_right_validate(maze: Maze, player: Player):
    """
    Check if moving right from the player's current position is a valid move within the maze.

    Args:
        maze (Maze): The Maze object representing the maze.
        player (Player): The Player object representing the player.

    Returns:
        bool: True if moving right is valid, False otherwise.
    """
    block_row, block_col = maze.get_block_number_index(player.block_number)
    curr_pos = (block_row, block_col, player.cell_row, player.cell_col)
    if player.cell_col == CELL_IN_BLOCK - 1 and block_col == maze.block_in_maze - 1:
        return False
    if player.cell_col < CELL_IN_BLOCK - 1:
        right_pos = (block_row, block_col, player.cell_row, player.cell_col + 1)
    elif player.cell_col == CELL_IN_BLOCK - 1 and block_col < maze.block_in_maze - 1:
        right_pos = (block_row, block_col + 1, player.cell_row, 0)
    return RIGHT in maze.block[curr_pos[0]][curr_pos[1]].cell[curr_pos[2]][curr_pos[3]].connect and \
           LEFT in maze.block[right_pos[0]][right_pos[1]].cell[right_pos[2]][right_pos[3]].connect

def show_text_in_button(window:pygame.Surface, surface:pygame.Surface, output_text:str, pos:tuple):
    """
    Display text on a button surface.

    Args:
        window (pygame.Surface): The window surface where the button will be displayed.
        surface (pygame.Surface): The surface representing the button.
        output_text (str): The text to display on the button.
        pos (tuple): The position of the button surface on the window.

    Returns:
        None
    """
    font = pygame.font.Font(pygame.font.get_default_font(), 25)
    if pos == (EXCHANGE_BLOCK_BUTTON_RECT_POS[0], EXCHANGE_BLOCK_BUTTON_RECT_POS[1]):
        surface.fill(RED)
        text = font.render(output_text , True , WHITE)
    else:
        surface.fill(WHITE)
        text = font.render(output_text , True , BLACK)
    
    text_width, text_height = text.get_rect().size
    surface.blit(text, ((surface.get_width()-text_width)/2,(surface.get_height()-text_height)/2))
    window.blit(surface, pos)
    # pygame.display.update()

def show_player_in_small_maze(window: pygame.Surface, small_maze: Maze):
    """
    Display the player in the small maze on the window.

    Args:
        window (pygame.Surface): The window surface where the player will be displayed.
        small_maze (Maze): The Maze object representing the small maze.

    Returns:
        None
    """
    red_circle_image = pygame.image.load("assets/image/red-circle.png")
    small_player_image = pygame.transform.smoothscale(red_circle_image, (small_maze.cell_size, small_maze.cell_size))
    window.blit(small_player_image, (SMALL_SCREEN_POS[0]+(SMALL_SCREEN_WIDTH)/2, SMALL_SCREEN_POS[1]+(SMALL_SCREEN_HEIGHT)/2))

def show_player_in_maze(window:pygame.Surface, image):
    """
    Display the player in the large maze on the window.

    Args:
        window (pygame.Surface): The window surface where the player will be displayed.
        image: The image representing the player.

    Returns:
        None
    """
    window.blit(image, (LARGE_SCREEN_POS[0]+(VISIBLE_WIDTH)/2, LARGE_SCREEN_POS[1]+(VISIBLE_HEIGHT)/2))

def show_number_in_middle_maze(window:pygame.Surface, middle_maze: Maze):
    """
    Display numbers in the middle maze.

    Args:
        window (pygame.Surface): The window surface where the numbers will be displayed.
        middle_maze (Maze): The Maze object representing the middle maze.

    Returns:
        None
    """
    block_size = middle_maze.cell_size * CELL_IN_BLOCK
    font = pygame.font.Font(pygame.font.get_default_font(), int(block_size * 0.8))
    
    for row in range(middle_maze.block_in_maze):
        for col in range(middle_maze.block_in_maze):
            rect = pygame.Rect(LARGE_SCREEN_POS[0]+col*block_size, LARGE_SCREEN_POS[1]+row*block_size,\
                                block_size, block_size)
            text = font.render(f"{row*middle_maze.block_in_maze+col}" , True , BLACK) 
            text.set_alpha(64)
            text_rect = text.get_rect(center=rect.center)
            window.blit(text, text_rect)

def show_player_in_middle_maze(window:pygame.Surface, middle_maze: Maze, player:Player):
    """
    Display the player in the middle maze on the window.

    Args:
        window (pygame.Surface): The window surface where the player will be displayed.
        middle_maze (Maze): The Maze object representing the middle maze.
        player (Player): The Player object representing the player.

    Returns:
        None
    """
    red_circle_image = pygame.image.load("assets/image/red-circle.png")
    middle_maze_player_image = pygame.transform.smoothscale(red_circle_image, (middle_maze.cell_size, middle_maze.cell_size))
    # window.blit(middle_maze_surface, LARGE_SCREEN_POS)
    block_row, block_col = middle_maze.get_block_number_index(player.block_number)
    block_size = middle_maze.cell_size * CELL_IN_BLOCK
    pos_x, pos_y = (block_col * block_size + player.cell_col * middle_maze.cell_size, \
                    block_row * block_size + player.cell_row * middle_maze.cell_size)
    window.blit(middle_maze_player_image, (LARGE_SCREEN_POS[0]+pos_x, LARGE_SCREEN_POS[1]+pos_y))

def show_mazes_and_players_in_game_mode(window, maze, maze_surface, small_maze, small_maze_surface, image):
    """
    Display mazes and players in the game mode on the window.

    Args:
        window: The window surface where the mazes and players will be displayed.
        maze: The large maze object.
        maze_surface: The surface representing the large maze.
        small_maze: The small maze object.
        small_maze_surface: The surface representing the small maze.
        image: The image representing the player.

    Returns:
        None
    """
    if image =="default":
        image = pygame.image.load("assets/image/move_right/frame_2.png")
    show_maze_on_window(maze, window, maze_surface, LARGE_SCREEN_POS)
    show_maze_on_window(small_maze, window, small_maze_surface, SMALL_SCREEN_POS)
    show_player_in_maze(window, image)
    show_player_in_small_maze(window, small_maze)
    
def show_mazes_and_players_in_exchange_mode(window, middle_maze, middle_maze_surface, small_maze, small_maze_surface, player):
    """
    Display the mazes and player in the exchange mode on the window.

    Args:
        window: The window surface where the mazes and players will be displayed.
        middle_maze: The middle maze object.
        middle_maze_surface: The surface representing the middle maze.
        small_maze: The small maze object.
        small_maze_surface: The surface representing the small maze.
        player: The player object.

    Returns:
        None
    """
    show_maze_on_window(middle_maze, window, middle_maze_surface, LARGE_SCREEN_POS)
    show_maze_on_window(small_maze, window, small_maze_surface, SMALL_SCREEN_POS)
    show_player_in_small_maze(window, small_maze)
    show_player_in_middle_maze(window, middle_maze, player)  
    show_number_in_middle_maze(window, middle_maze) 

def center_player_on_maze(player:Player, maze:Maze):
    """
    Center the player on the maze.

    Args:
        player: The player object.
        maze: The maze object.

    Returns:
        None
    """
    maze.reset_pos()
    block_row, block_col = maze.get_block_number_index(player.block_number)
    # print(block_row, block_col)
    pos_x = block_col * maze.cell_size * CELL_IN_BLOCK + player.cell_col * maze.cell_size
    pos_y = block_row * maze.cell_size * CELL_IN_BLOCK + player.cell_row * maze.cell_size
    if maze.cell_size == SMALL_MAZE_CELL_SIZE:
        maze.move(-pos_x + (SMALL_SCREEN_WIDTH)/2, -pos_y + (SMALL_SCREEN_HEIGHT)/2)
    else:
        maze.move(-pos_x + (VISIBLE_WIDTH)/2, -pos_y + (VISIBLE_HEIGHT)/2)
        
def update_player_on_step_change(player:Player):
    """
    Minus player life according to the step count.

    Args:
        player: The player object.

    Returns:
        None
    """
    if player.step % STEP_COUNT == 0:
        sound_effect = pygame.mixer.Sound('assets/sounds/hurt.wav')
        sound_effect.play()
        player.life -= 1
        
def create_easy_enemy(player:Player, block_in_maze, pos_set:set):
    """
    Create easy enemies.

    Args:
        player: The player object.
        block_in_maze: The number of blocks in each row and column of the maze.
        pos_set: The set of positions.

    Returns:
        dict: Dictionary of easy enemies.
    """
    global my_seed
    enemy_dict = {}
    for name in EASY_ENEMY_LIST:
        image_path = f"assets/image/enemy/{name}/{name}.png"
        attack = 10 + random.choice([-1,0,1])
        my_seed += 1
        defense = 3 + random.choice([-1,0,1])
        my_seed += 1
        life = 250 + random.choice([-1,0,1]) * 20
        my_seed += 1
        attack_dice = Dice(1,3)
        defense_dice = Dice(1,3)
        my_seed += 1
        pos = (random.choice(range(block_in_maze)),random.choice(range(block_in_maze)),random.choice(range(CELL_IN_BLOCK)),random.choice(range(CELL_IN_BLOCK)))
        
        # Generate random position for the enemy ensuring uniqueness
        while pos in pos_set:
            my_seed += 1
            pos = (random.choice(range(block_in_maze)),random.choice(range(block_in_maze)),random.choice(range(CELL_IN_BLOCK)),random.choice(range(CELL_IN_BLOCK)))
        pos_set.add(pos)
        block_number = pos[0] * block_in_maze + pos[1]
        key = (block_number, pos[2], pos[3])
        enemy = Enemy(name, life, attack, defense, attack_dice, defense_dice, pos, block_in_maze, image_path, key)
        enemy_dict[key] = enemy
        
    return enemy_dict

def create_medium_enemy(player:Player, block_in_maze, pos_set:set):
    """
    Create medium enemies.

    Args:
        player: The player object.
        block_in_maze: The number of blocks in each row and column of the maze.
        pos_set: The set of positions.

    Returns:
        dict: Dictionary of medium enemies.
    """
    global my_seed
    my_seed += 1
    enemy_dict = {}
    for name in MEDIUM_ENEMY_LIST:
        image_path = f"assets/image/enemy/{name}/{name}.png"
        attack = 13 + random.choice([-1,0,1])
        my_seed += 1
        defense = 4 + random.choice([-1,0,1])
        my_seed += 1
        life = 400 + random.choice([-1,0,1]) * 20
        my_seed += 1
        attack_dice = Dice(1,4)
        defense_dice = Dice(1,4)
        
        # Generate random position for the enemy ensuring uniqueness
        pos = (random.choice(range(block_in_maze)),random.choice(range(block_in_maze)),random.choice(range(CELL_IN_BLOCK)),random.choice(range(CELL_IN_BLOCK)))
        while pos in pos_set:
            my_seed += 1
            pos = (random.choice(range(block_in_maze)),random.choice(range(block_in_maze)),random.choice(range(CELL_IN_BLOCK)),random.choice(range(CELL_IN_BLOCK)))
        block_number = pos[0] * block_in_maze + pos[1]
        key = (block_number, pos[2], pos[3])
        enemy = Enemy(name, life, attack, defense, attack_dice, defense_dice, pos, block_in_maze, image_path, key)
        enemy_dict[key] = enemy
        my_seed += 1
    return enemy_dict

def create_hard_enemy(player:Player, block_in_maze, pos_set:set):
    """
    Create hard enemies.

    Args:
        player: The player object.
        block_in_maze: The number of blocks in each row and column of the maze.
        pos_set: The set of positions.

    Returns:
        dict: Dictionary of hard enemies.
    """
    global my_seed
    my_seed += 1
    enemy_dict = {}
    for name in HARD_ENEMY_LIST:
        image_path = f"assets/image/enemy/{name}/{name}.png"
        attack = 15 + random.choice([-1,0,1])
        my_seed += 1
        defense = 5 + random.choice([-1,0,1])
        my_seed += 1
        life = 500 + random.choice([-1,0,1]) * 20
        my_seed += 1
        attack_dice = Dice(1,6)
        defense_dice = Dice(1,6)
        
        # Generate random position for the enemy ensuring uniqueness
        pos = (random.choice(range(block_in_maze)),random.choice(range(block_in_maze)),random.choice(range(CELL_IN_BLOCK)),random.choice(range(CELL_IN_BLOCK)))
        while pos in pos_set:
            my_seed += 1
            pos = (random.choice(range(block_in_maze)),random.choice(range(block_in_maze)),random.choice(range(CELL_IN_BLOCK)),random.choice(range(CELL_IN_BLOCK)))
        block_number = pos[0] * block_in_maze + pos[1]
        key = (block_number, pos[2], pos[3])
        enemy = Enemy(name, life, attack, defense, attack_dice, defense_dice, pos, block_in_maze, image_path, key)
        enemy_dict[key] = enemy
        my_seed += 1
    return enemy_dict

def check_show_enemy(player:Player, maze:Maze, enemy:Enemy):
    """
    Check if an enemy should be shown on the screen based on the player's position and maze.

    Args:
        player: The player object.
        maze: The Maze object.
        enemy: The Enemy object to check.

    Returns:
        bool: True if the enemy should be shown, False otherwise.
    """
    if enemy.defeated:
        return False
    if maze.cell_size == SMALL_MAZE_CELL_SIZE and enemy.visible == False:
        return False
    enemy_pos_x, enemy_pos_y = enemy.get_absolute_pos(maze)
    player_pos_x, player_pos_y = player.get_absolute_pos(maze)
    
    if maze.cell_size == SMALL_MAZE_CELL_SIZE:
        x_condition = player_pos_x-8*maze.cell_size <= enemy_pos_x <= player_pos_x+7*maze.cell_size 
        y_condition = player_pos_y-8*maze.cell_size <= enemy_pos_y <= player_pos_y+7*maze.cell_size
    else:
        x_condition = player_pos_x-4*maze.cell_size <= enemy_pos_x <= player_pos_x+3*maze.cell_size 
        y_condition = player_pos_y-4*maze.cell_size <= enemy_pos_y <= player_pos_y+3*maze.cell_size

    return x_condition and y_condition

def show_enemy_in_maze(enemy_dict:dict[tuple,Enemy], maze:Maze, window:pygame.Surface, player:Player):
    """
    Show enemies on the maze.

    Args:
        enemy_dict: Dictionary containing enemy positions and Enemy objects.
        maze: The Maze object.
        window: The pygame window.
        player: The player object.
    """
    for enemy in enemy_dict.values():
        if maze.cell_size == SMALL_MAZE_CELL_SIZE:
            image = pygame.image.load("assets/image/danger.png")
            enemy_image = pygame.transform.smoothscale(image, (maze.cell_size, maze.cell_size))
        else:
            image = pygame.image.load(enemy.image_path)
            enemy_image = pygame.transform.smoothscale(image, (maze.cell_size, maze.cell_size))
        if check_show_enemy(player, maze, enemy):
            enemy.visible = True
            enemy_pos_x, enemy_pos_y = enemy.get_absolute_pos(maze)
            player_pos_x, player_pos_y = player.get_absolute_pos(maze)
            if maze.cell_size == SMALL_MAZE_CELL_SIZE:
                screen_middle_x = SMALL_SCREEN_POS[0]+(SMALL_SCREEN_WIDTH)/2
                screen_middle_y = SMALL_SCREEN_POS[1]+(SMALL_SCREEN_HEIGHT)/2
            else:
                screen_middle_x = LARGE_SCREEN_POS[0]+(VISIBLE_WIDTH)/2
                screen_middle_y = LARGE_SCREEN_POS[1]+(VISIBLE_HEIGHT)/2
            window.blit(enemy_image, (screen_middle_x+(enemy_pos_x-player_pos_x), screen_middle_y+(enemy_pos_y-player_pos_y)))
    
def show_enemy_in_middle_maze(window:pygame.Surface, middle_maze:Maze, enemy_dict:dict[tuple,Enemy]):
    """
    Show enemies in the middle maze.

    Args:
        window: The pygame window.
        middle_maze: The middle maze object.
        enemy_dict: Dictionary containing enemy positions and Enemy objects.
    """
    for enemy in enemy_dict.values():
        if enemy.visible == False or enemy.defeated == True:
            continue
        
        image = pygame.image.load("assets/image/danger.png")
        enemy_image = pygame.transform.smoothscale(image, (middle_maze.cell_size, middle_maze.cell_size))
        pos_x, pos_y = enemy.get_absolute_pos(middle_maze)
        window.blit(enemy_image, (LARGE_SCREEN_POS[0]+pos_x, LARGE_SCREEN_POS[1]+pos_y))
        
def show_enemy_attribute_icon(window:pygame.Surface):
    """
    Show icons representing enemy attributes.

    Args:
        window: The pygame window.
    """
    icon_list = ENEMY_ICON_LIST
    images = {}

    for icon in icon_list:
        image_path = f"assets/image/{icon}.png"
        images[icon] = load_and_resize_image(image_path, (PLAYER_INFORMATION_IMAGE_SIZE, PLAYER_INFORMATION_IMAGE_SIZE))
       
    positions = {}
    y_offset = 0
    x_offsets = [0, 120]  # x offsets for the first and second column

    # Iterate over image names and create positions dynamically
    for idx, icon in enumerate(icon_list):
        x_offset = x_offsets[idx // 3]  # Determine the x offset based on the column
        y_offset = (idx % 3) * 30  # Calculate the y offset based on the row
        positions[icon] = (ENEMY_INFORMATION_POS[0] + x_offset, ENEMY_INFORMATION_POS[1] + y_offset)
    
    for icon, image in images.items():
        window.blit(image, positions[icon])

def show_enemy_attribute_value(window:pygame.Surface, enemy:Enemy):
    """
    Show values of enemy attributes on the screen.

    Args:
        window: The pygame window.
        enemy: The Enemy object whose attributes need to be displayed.
    """
    font = pygame.font.Font(pygame.font.get_default_font(), 25)
    text_list = [f"{enemy.life}", f"{enemy.attack}", f"{enemy.defense}", f"{enemy.fame}", \
                f"{enemy.attack_dice.lower_bound}~{enemy.attack_dice.upper_bound}",\
                f"{enemy.defense_dice.lower_bound}~{enemy.defense_dice.upper_bound}"]
    y_offset = 0
    x_offsets = [0, 120]  # x offsets for the first and second column
    for idx, text in enumerate(text_list):
        x_offset = x_offsets[idx // 3]  # Determine the x offset based on the column
        y_offset = (idx % 3) * 30  # Calculate the y offset based on the row
        rect = pygame.Rect(ENEMY_INFORMATION_TEXT_RECT_POS[0]+x_offset, ENEMY_INFORMATION_TEXT_RECT_POS[1]+y_offset,\
                            ENEMY_INFORMATION_TEXT_RECT_POS[2], ENEMY_INFORMATION_TEXT_RECT_POS[3])
        text = font.render(text , True , BLACK)
        text_rect = text.get_rect(center=rect.center)
        pygame.draw.rect(window, LIGHT_GRAY, rect)
        window.blit(text, text_rect)
        
def show_player_attribute_icon_in_battle(window:pygame.Surface):
    """
    Show icons representing player attributes in battle mode.

    Args:
        window: The pygame window.
    """
    icon_list = ENEMY_ICON_LIST
    images = {}

    for icon in icon_list:
        image_path = f"assets/image/{icon}.png"
        images[icon] = load_and_resize_image(image_path, (PLAYER_INFORMATION_IMAGE_SIZE, PLAYER_INFORMATION_IMAGE_SIZE))
       
    positions = {}
    y_offset = 0
    x_offsets = [0, 120]  # x offsets for the first and second column

    # Iterate over image names and create positions dynamically
    for idx, icon in enumerate(icon_list):
        x_offset = x_offsets[idx // 3]  # Determine the x offset based on the column
        y_offset = (idx % 3) * 30  # Calculate the y offset based on the row
        positions[icon] = (PLAYER_INFORMATION_BATTLE_POS[0] + x_offset, PLAYER_INFORMATION_BATTLE_POS[1] + y_offset)
    
    for icon, image in images.items():
        window.blit(image, positions[icon])

def show_player_attribute_value_in_battle(window:pygame.Surface, player:Player):
    """
    Show values of player attributes in battle mode on the screen.

    Args:
        window: The pygame window.
        player: The Player object whose attributes need to be displayed.
    """
    font = pygame.font.Font(pygame.font.get_default_font(), 25)
    text_list = [f"{player.life}", f"{player.attack}", f"{player.defense}", f"{player.fame}", \
                f"{player.attack_dice.lower_bound}~{player.attack_dice.upper_bound}",\
                f"{player.defense_dice.lower_bound}~{player.defense_dice.upper_bound}"]
    y_offset = 0
    x_offsets = [0, 120]  # x offsets for the first and second column
    for idx, text in enumerate(text_list):
        x_offset = x_offsets[idx // 3]  # Determine the x offset based on the column
        y_offset = (idx % 3) * 30  # Calculate the y offset based on the row
        rect = pygame.Rect(PLAYER_INFORMATION_TEXT_BATTLE_RECT_POS[0]+x_offset, PLAYER_INFORMATION_TEXT_BATTLE_RECT_POS[1]+y_offset,\
                            PLAYER_INFORMATION_TEXT_BATTLE_RECT_POS[2], PLAYER_INFORMATION_TEXT_BATTLE_RECT_POS[3])
        text = font.render(text , True , BLACK)
        text_rect = text.get_rect(center=rect.center)
        pygame.draw.rect(window, LIGHT_GRAY, rect)
        window.blit(text, text_rect)

def show_turn_icon(window:pygame.Surface, turn:str):
    """
    Show turn icons indicating whether it's the player's or enemy's turn.

    Args:
        window: The pygame window.
        turn: A string representing whose turn it is ("attack" or "defense").
    """
    player_turn_pos = (850, 550)
    enemy_turn_pos = (510, 550)
    sword_image = load_and_resize_image("assets/image/sword.png", (TURN_ICON_IMAGE_SIZE, TURN_ICON_IMAGE_SIZE))
    defense_image = load_and_resize_image("assets/image/defense.png", (TURN_ICON_IMAGE_SIZE, TURN_ICON_IMAGE_SIZE))
    if turn == "attack":
        window.blit(sword_image, player_turn_pos)
        window.blit(defense_image, enemy_turn_pos)
    else:
        window.blit(defense_image, player_turn_pos)
        window.blit(sword_image, enemy_turn_pos)       
        
def update_player_attribute_after_winning_battle(player:Player, enemy:Enemy):
    """
    Update player's attributes after winning a battle.

    Args:
        player: The Player object.
        enemy: The Enemy object defeated by the player.
    """
    enemy.defeated = True
    player.attack += enemy.attack // 10
    player.defense += enemy.defense // 5
    player.maximum_life += enemy.initial_life // 10
    player.life += enemy.initial_life // 10
    player.fame += enemy.fame
    
def use_skill_during_battle(player:Player, enemy:Enemy, window:pygame.Surface, helper:Helper):
    """
    Use a skill during battle mode.

    Args:
        player: The Player object.
        enemy: The Enemy object being battled.
        window: The pygame window.
        helper: The Helper object representing the skill being used.
    """
    helper_param_dict = update_helper_param(player, enemy)
    helper.use_skill(*helper_param_dict[helper.name])
    helper.reduce_remaining_rounds()
    if helper.rounds <= 0:
        helper.activate = False
    show_enemy_attribute_value(window, enemy)
    show_player_attribute_value_in_battle(window, player)
    show_player_attribute_value(window, player)
    
def use_skill_in_game_mode(player:Player, window:pygame.Surface, helper:Helper):
    """
    Use a skill in game mode.

    Args:
        player: The Player object.
        window: The pygame window.
        helper: The Helper object representing the skill being used.
    """
    helper_param_dict = update_helper_param(player, None)
    helper.use_skill(*helper_param_dict[helper.name])
    helper.reduce_remaining_rounds()
    if helper.rounds <= 0:
        helper.activate = False
    show_player_attribute_value(window, player)
    
def update_helper_activate(helper_dict:dict[str,Helper]):
    """
    Update the activation status of helpers. (Use after battle)

    Args:
        helper_dict: A dictionary containing helper objects.
    """
    for helper in helper_dict.values():
        if helper.activate and "game" not in helper.allow_mode:
            helper.activate = False

def show_helper_effect(window:pygame.Surface, helper:Helper):
    """
    Display the visual effect of a helper's skill.

    Args:
        window: The pygame window.
        helper: The Helper object whose effect is being displayed.
    """
    pygame.mixer.set_num_channels(2)
    voice = pygame.mixer.Channel(1)
    image = load_and_resize_image(f"assets/image/portrait/{helper.name}_effect.jpg", (730, 730))
    window.blit(image, (LARGE_SCREEN_POS[0], LARGE_SCREEN_POS[1]))
    pygame.display.update()
    sound_effect = pygame.mixer.Sound(f'assets/sounds/{helper.name}_effect.wav')
    voice.play(sound_effect)
    while voice.get_busy():
        continue
    
def show_player_damage(window:pygame.Surface, player_damage):
    """
    Display the damage taken by the player.

    Args:
        window: The pygame window.
        player_damage: The amount of damage taken by the player.
    """
    font = pygame.font.Font(pygame.font.get_default_font(), 25)
    text = font.render(f"-{player_damage}", True , RED)
    rect = pygame.Rect(PLAYER_DAMAGE_RECT_POS)
    text_rect = text.get_rect(center=rect.center)
    window.blit(text, text_rect)
    pygame.display.update()
    
def show_enemy_damage(window:pygame.Surface, enemy_damage):
    """
    Display the damage taken by the enemy.

    Args:
        window: The pygame window.
        enemy_damage: The amount of damage taken by the enemy.
    """
    font = pygame.font.Font(pygame.font.get_default_font(), 25)
    text = font.render(f"-{enemy_damage}", True , RED)
    rect = pygame.Rect(ENEMY_DAMAGE_RECT_POS)
    text_rect = text.get_rect(center=rect.center)
    window.blit(text, text_rect)
    pygame.display.update()
         
def handle_helper_effect(window:pygame.Surface, helper_dict:dict[str,Helper], enemy:Enemy, player:Player, execution_time:str, mode:str):
    """
    Handle the effect of a helper's skill during battle.

    Args:
        window: The pygame window.
        helper_dict: A dictionary containing helper objects.
        enemy: The Enemy object being battled.
        player: The Player object.
        execution_time: The time at which the skill is executed.
    
    Returns:
        str: The result of the battle ("win" if enemy is defeated, None otherwise).
    """
    for helper in helper_dict.values():
        if helper.activate and helper.skill_execution_time == execution_time:
            use_skill_during_battle(player, enemy, window, helper)
            show_helper(window, helper_dict, player, mode)
        if enemy.life <= 0:
            update_player_attribute_after_winning_battle(player, enemy)
            update_helper_activate(helper_dict)
            return "win"
        if enemy.defeated:
            update_helper_activate(helper_dict)
            return "win" 
   
def battle(player:Player, enemy:Enemy, window:pygame.Surface, helper_dict:dict[str,Helper], helper_rect_dict:dict[str, pygame.Rect]):
    """
    Function to handle the battle between the player and an enemy.

    Args:
        player (Player): The player object.
        enemy (Enemy): The enemy object.
        window (pygame.Surface): The pygame window.
        helper_dict (dict): Dictionary containing helper objects.
        helper_rect_dict (dict): Dictionary containing helper rectangles.
    """
    mode = "battle"
    cursor_state = "arrow"
    turn = "attack"
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    # Load and play the battle music
    pygame.mixer.music.load('assets/sounds/Luffy Fierce Attack.mp3')
    pygame.mixer.music.play(-1)
    
    # Load and display battle background image
    battle_background_image = load_and_resize_image("assets/image/battle_background.png", (VISIBLE_WIDTH+5, VISIBLE_HEIGHT+5))
    window.blit(battle_background_image, LARGE_SCREEN_POS)
    
    # Display the enemy image
    enemy_image = load_and_resize_image(enemy.image_path, (BATTLE_PLAYER_IMAGE_SIZE, BATTLE_PLAYER_IMAGE_SIZE)) 
    window.blit(enemy_image, (460, 600))
    
    # Display player image
    player_image = load_and_resize_image("assets/image/move_left/frame_2.png", (BATTLE_PLAYER_IMAGE_SIZE, BATTLE_PLAYER_IMAGE_SIZE))
    window.blit(player_image, (800, 600))
    
    # Display instruction for rolling dice
    font = pygame.font.Font(pygame.font.get_default_font(), 25)
    text = font.render("Press R To Roll Dice", True , BLACK)
    text_width, text_height = text.get_rect().size
    window.blit(text, (LARGE_SCREEN_POS[0]+20+(VISIBLE_WIDTH-text_width)//2,280))
    
    # Display turn icon, player and enemy attribute icons, and their values
    show_turn_icon(window, turn)
    show_helper(window, helper_dict, player, mode)
    show_enemy_attribute_icon(window)
    show_enemy_attribute_value(window, enemy)
    show_player_attribute_icon_in_battle(window)
    show_player_attribute_value_in_battle(window, player)
    
    pygame.display.update()
    pygame.image.save(window, "./output/Battle.jpeg")
    
    
    running = True 
    global my_seed
    
    while running:
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and turn == "attack":
                    
                    # Handle the effect of helper skill before player's attack
                    result = handle_helper_effect(window, helper_dict, enemy, player, "before_attack", mode)
                    if result == "win":
                        return
                        
                    # Roll dice for player's attack and enemy's defense
                    player_attack_dice = player.attack_dice.roll_dice()
                    enemy_defense_dice = enemy.defense_dice.roll_dice()
                    enemy_defense_image = load_and_resize_image(f"assets/image/enemy/{enemy.name}/defend.png", (BATTLE_PLAYER_IMAGE_SIZE, BATTLE_PLAYER_IMAGE_SIZE))
                    
                    # Display frames for player's attack animation
                    frames_folder = "./assets/image/attack"
                    frame_files = [f"{frames_folder}/attack_{i}.png" for i in range(1, 4)]
                    frames = [load_and_resize_image(file, (BATTLE_PLAYER_IMAGE_SIZE, BATTLE_PLAYER_IMAGE_SIZE)) for file in frame_files]
                    for image, pos in zip(frames, PLAYER_ATTACK_POS_LIST):
                        window.blit(battle_background_image, LARGE_SCREEN_POS)
                        if image == frames[-1]:
                            window.blit(enemy_defense_image, (460, 600))
                        else:
                            window.blit(enemy_image, (460, 600))
                        window.blit(image, pos)
                        window.blit(text, (LARGE_SCREEN_POS[0]+20+(VISIBLE_WIDTH-text_width)//2,280))
                        show_enemy_attribute_value(window, enemy)
                        show_enemy_attribute_icon(window)
                        show_player_attribute_value_in_battle(window, player)
                        show_player_attribute_icon_in_battle(window)
                        show_player_attribute_value(window, player)
                        show_turn_icon(window, turn)
                        pygame.display.update()
                        # pygame.time.delay(DELAY_TIME)
                     
                    # Calculate player's damage to the enemy   
                    player_damage = player.attack * player_attack_dice - enemy.defense * enemy_defense_dice
                    if player_damage < 0:
                        player_damage = 0
                    show_player_damage(window, player_damage)
                    sound_effect = pygame.mixer.Sound('assets/sounds/attack.wav')
                    sound_effect.play()
                    time.sleep(0.5)
                    
                    # Update enemy's life after player's attack
                    enemy.life -= player_damage
                    if enemy.life <= 0:
                        update_player_attribute_after_winning_battle(player, enemy)
                        update_helper_activate(helper_dict)
                        return 
                    
                    # Handle the effect of helper skill after player's attack
                    result = handle_helper_effect(window, helper_dict, enemy, player, "after_attack", mode)
                    if result == "win":
                        return
                    
                    # Change turn to defense
                    turn = "defense"
                    
                elif event.key == pygame.K_r and turn == "defense":
                    # Handle the effect of helper skill before enemy's attack
                    result = handle_helper_effect(window, helper_dict, enemy, player, "before_defense", mode)
                    if result == "win":
                        return
                    
                    # Roll dice for player's defense and enemy's attack
                    player_defense_dice = player.defense_dice.roll_dice()
                    enemy_attack_dice = enemy.attack_dice.roll_dice()
                    player_defense_image = load_and_resize_image(f"assets/image/defend.png", (BATTLE_PLAYER_IMAGE_SIZE, BATTLE_PLAYER_IMAGE_SIZE))
                    frame_files = [f"./assets/image/enemy/{enemy.name}/attack_{i}.png" for i in range(1, 4)]
                    frames = [load_and_resize_image(file, (BATTLE_PLAYER_IMAGE_SIZE, BATTLE_PLAYER_IMAGE_SIZE)) for file in frame_files]
                    for image, pos in zip(frames, ENEMY_ATTACK_POS_LIST):
                        window.blit(battle_background_image, LARGE_SCREEN_POS)
                        if image == frames[-1]:
                            window.blit(player_defense_image, (800, 600))
                        else:
                            window.blit(player_image, (800, 600))
                        window.blit(image, pos)
                        window.blit(text, (LARGE_SCREEN_POS[0]+20+(VISIBLE_WIDTH-text_width)//2,280))
                        show_enemy_attribute_value(window, enemy)
                        show_enemy_attribute_icon(window)
                        show_player_attribute_value_in_battle(window, player)
                        show_player_attribute_icon_in_battle(window)
                        show_player_attribute_value(window, player)
                        show_turn_icon(window, turn)
                        pygame.display.update()
                        
                    # Calculate enemy's damage to the player
                    enemy_damage = enemy.attack * enemy_attack_dice - player.defense * player_defense_dice
                    if enemy_damage < 0:
                        enemy_damage = 0
                    show_enemy_damage(window, enemy_damage)
                    sound_effect = pygame.mixer.Sound('assets/sounds/hurt.wav')
                    sound_effect.play()
                    time.sleep(0.5)
                    player.life -= enemy_damage
                    
                    # Handle the effect of helper skill after enemy's attack
                    result = handle_helper_effect(window, helper_dict, enemy, player, "after_defense", mode)
                    if result == "win":
                        return
                    
                    # Check if player's life is below 0
                    if player.life <= 0:
                        return
                    
                    turn = "attack"
                
                # Redraw the battle scene after each action
                window.blit(battle_background_image, LARGE_SCREEN_POS)
                window.blit(enemy_image, (460, 600))
                window.blit(player_image, (800, 600))
                window.blit(text, (LARGE_SCREEN_POS[0]+20+(VISIBLE_WIDTH-text_width)//2,280))
                show_enemy_attribute_value(window, enemy)
                show_enemy_attribute_icon(window)
                show_player_attribute_value_in_battle(window, player)
                show_player_attribute_icon_in_battle(window)
                show_player_attribute_value(window, player)
                show_turn_icon(window, turn)
                pygame.display.update()
                
                # Reset enemy's defense and attack attributes
                enemy.defense = enemy.initial_defense
                enemy.attack = enemy.initial_attack
                # print(enemy.life, player.life)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Play sound effect on mouse click
                sound_effect = pygame.mixer.Sound('assets/sounds/mouse-click.mp3')
                sound_effect.play()
                
                # Check if a helper is clicked and available, then activate it
                for name, helper in helper_dict.items():
                    if helper_rect_dict[name].collidepoint(event.pos) and check_helper_validate(player, mode, helper):
                        helper.activate = True
                        helper.available = False
                        player.coin -= helper.cost
                        show_player_attribute_value(window, player)
                        show_helper(window, helper_dict, player, mode)
                        show_helper_effect(window, helper)
                        pygame.display.update()
                        
                        # Handle the effect of helper skill right away
                        result = handle_helper_effect(window, helper_dict, enemy, player, "right_away", mode)
                        if result == "win":
                            return      
                         
                # Redraw the battle scene after each action
                window.blit(battle_background_image, LARGE_SCREEN_POS)
                window.blit(enemy_image, (460, 600))
                window.blit(player_image, (800, 600))
                window.blit(text, (LARGE_SCREEN_POS[0]+20+(VISIBLE_WIDTH-text_width)//2,280))
                show_enemy_attribute_value(window, enemy)
                show_enemy_attribute_icon(window)
                show_player_attribute_value_in_battle(window, player)
                show_player_attribute_icon_in_battle(window)
                show_player_attribute_value(window, player)
                show_turn_icon(window, turn)
                pygame.display.update()
        
        new_cursor_state = "arrow"         
            
        # Change cursor to hand icon if hovering over a helper and validate
        for helper, helper_rect in helper_rect_dict.items():
            if helper_rect.collidepoint(pygame.mouse.get_pos()) and check_helper_validate(player, mode, helper_dict[helper]):
                new_cursor_state = "hand"
        
        if new_cursor_state != cursor_state:
            if new_cursor_state == "hand":
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            cursor_state = new_cursor_state
                    
def load_and_resize_image(image_path, size):
    """
    Load an image from the given path and resize it to the specified size.

    Args:
        image_path (str): The path to the image file.
        size (tuple): The size to resize the image to.

    Returns:
        pygame.Surface: The resized image.
    """
    image = pygame.image.load(image_path).convert_alpha()
    resize_image = pygame.transform.smoothscale(image, size)
    return resize_image

def show_player_attribute_value(window:pygame.Surface, player:Player):
    """
    Display player attribute values on the game window.

    Args:
        window (pygame.Surface): The pygame window.
        player (Player): The player object.
    """
    font = pygame.font.Font(pygame.font.get_default_font(), 25)
    text_list = [f"{player.life}/{player.maximum_life}", f"{player.attack}", f"{player.defense}", f"{player.step}",\
                f"{player.coin}", f"{player.attack_dice.lower_bound}~{player.attack_dice.upper_bound}",\
                f"{player.defense_dice.lower_bound}~{player.defense_dice.upper_bound}", f"{player.fame}"]
    y_offset = 0
    x_offsets = [0, 120]  # x offsets for the first and second column
    for idx, text in enumerate(text_list):
        x_offset = x_offsets[idx // 4]  # Determine the x offset based on the column
        y_offset = (idx % 4) * 30  # Calculate the y offset based on the row
        rect = pygame.Rect(PLAYER_INFORMATION_TEXT_RECT_POS[0]+x_offset, PLAYER_INFORMATION_TEXT_RECT_POS[1]+y_offset,\
                            PLAYER_INFORMATION_TEXT_RECT_POS[2], PLAYER_INFORMATION_TEXT_RECT_POS[3])
        if idx == 0 and player.life <= player.maximum_life // 5:
            text = font.render(text , True , RED)
        else:
            text = font.render(text , True , BLACK)
        text_rect = text.get_rect(center=rect.center)
        pygame.draw.rect(window, LIGHT_BROWN, rect)
        window.blit(text, text_rect)

def show_player_attribute_icon(window:pygame.Surface):
    """
    Display icons representing player attributes on the game window.

    Args:
        window (pygame.Surface): The pygame window.
    """
    icon_list = ICON_LIST
    images = {}

    for icon in icon_list:
        image_path = f"assets/image/{icon}.png"
        images[icon] = load_and_resize_image(image_path, (PLAYER_INFORMATION_IMAGE_SIZE, PLAYER_INFORMATION_IMAGE_SIZE))
       
    positions = {}
    y_offset = 0
    x_offsets = [0, 120]  # x offsets for the first and second column

    # Iterate over image names and create positions dynamically
    for idx, icon in enumerate(icon_list):
        x_offset = x_offsets[idx // 4]  # Determine the x offset based on the column
        y_offset = (idx % 4) * 30  # Calculate the y offset based on the row
        positions[icon] = (PLAYER_INFORMATION_POS[0] + x_offset, PLAYER_INFORMATION_POS[1] + y_offset)
    
    for icon, image in images.items():
        window.blit(image, positions[icon])
        
def show_helper(window:pygame.Surface, helper_dict:dict[str,Helper], player:Player, mode:str):
    """
    Display helper portraits and their activation status on the game window.

    Args:
        window (pygame.Surface): The pygame window.
        helper_dict (dict): Dictionary containing helper objects.
    """
    helper_list = HELPER_LIST
    images = {}

    for helper in helper_list:
        if check_helper_validate(player, mode, helper_dict[helper]):
            image_path = f"assets/image/portrait/{helper}.png"
        else:
            image_path = f"assets/image/portrait/bw_{helper}.png"
     
        images[helper] = load_and_resize_image(image_path, (HELPER_PORTRAIT_SIZE, HELPER_PORTRAIT_SIZE))
       
    positions = {}
    y_offsets = [0, 95]
    x_offset = 0  

    # Iterate over image names and create positions dynamically
    for idx, helper in enumerate(helper_list):
        x_offset = (idx % 3) * 80
        y_offset = y_offsets[idx // 3]  # Calculate the y offset based on the row
        positions[helper] = (HELPER_PORTRAIT_POS[0] + x_offset, HELPER_PORTRAIT_POS[1] + y_offset)
    
    for helper, image in images.items():
        window.blit(image, positions[helper])
        if helper_dict[helper].activate:
            pygame.draw.rect(window, RED, (positions[helper][0], positions[helper][1],\
                                            HELPER_PORTRAIT_SIZE, HELPER_PORTRAIT_SIZE), 3)

def show_helper_cost(window:pygame.Surface, helper_dict:dict[str,Helper]):
    """
    Display the cost of each helper on the game window.

    Args:
        window (pygame.Surface): The pygame window.
        helper_dict (dict): Dictionary containing helper objects.
    """
    image_path = f"assets/image/coin.png"
    coin_image = load_and_resize_image(image_path, (HELPER_COIN_SIZE, HELPER_COIN_SIZE))
        
    font = pygame.font.Font(pygame.font.get_default_font(), 15)
    text_list = []
    for helper in helper_dict.values():
        text_list.append(f"{helper.cost}")
        
    y_offsets = [0, 95]
    x_offset = 0
    for idx, text in enumerate(text_list):
        x_offset = (idx % 3) * 80
        y_offset = y_offsets[idx // 3]  # Calculate the y offset based on the row
        rect = pygame.Rect(HELPER_RECT_POS[0]+x_offset, HELPER_RECT_POS[1]+y_offset,\
                            HELPER_RECT_POS[2], HELPER_RECT_POS[3])
        text = font.render(text , True , BLACK)
        text_rect = text.get_rect(center=rect.center)
        top_right_corner = text_rect.topright
        # pygame.draw.rect(window, LIGHT_BROWN, rect)
        window.blit(text, text_rect)
        # Show the coin after the cost text
        window.blit(coin_image, (top_right_corner[0]+5, top_right_corner[1]))
              
def create_helper():
    """
    Create helper objects and store them in a dictionary.

    Returns:
        dict: A dictionary containing helper objects with helper names as keys.
    """
    helper_dict = {}
    helper_dict["Zoro"] = Helper("Zoro", 10, skill.never_die, 3, ["game", "battle"], "after_defense")
    helper_dict["Sanji"] = Helper("Sanji", 8, skill.huge_damage, 1, ["battle"], "right_away")
    helper_dict["Nami"] = Helper("Nami", 8, skill.remove_defense, 5, ["battle"], "before_attack")
    helper_dict["Usopp"] = Helper("Usopp", 6, skill.escape, 1, ["battle"], "right_away")
    helper_dict["Chopper"] = Helper("Chopper", 3, skill.add_life, 10, ["game", "battle"], "before_attack")
    helper_dict["Brook"] = Helper("Brook", 7, skill.half_the_attack, 3, ["battle"], "before_attack")
    return helper_dict

def create_helper_rect_dict():
    helper_rect_dict = {}
    y_offsets = [0, 95]
    x_offset = 0
    for idx, helper in enumerate(HELPER_LIST):
        x_offset = (idx % 3) * 80
        y_offset = y_offsets[idx // 3]
        helper_rect_dict[helper] = pygame.Rect((HELPER_PORTRAIT_POS[0]+x_offset, HELPER_PORTRAIT_POS[1]+y_offset,\
                                                    HELPER_PORTRAIT_SIZE, HELPER_PORTRAIT_SIZE))
    return helper_rect_dict
    

def update_helper_param(player:Player, enemy:Enemy):
    """
    Update helper skill parameters based on the player and enemy attributes.

    Args:
        player (Player): The player object.
        enemy (Enemy): The enemy object.

    Returns:
        dict: A dictionary containing helper parameters with helper names as keys.
    """
    helper_param_dict = {}
    helper_param_dict["Zoro"] = [player]
    helper_param_dict["Sanji"] = [player, enemy]
    helper_param_dict["Nami"] = [enemy]
    helper_param_dict["Usopp"] = [player, enemy]
    helper_param_dict["Chopper"] = [player, player.maximum_life//5]
    helper_param_dict["Brook"] = [enemy]
    return helper_param_dict
   
def check_helper_validate(player:Player, mode:str, helper:Helper):
    """
    Check if a helper is valid for activation.

    Args:
        player (Player): The player object.
        mode (str): The current game mode.
        helper (Helper): The helper object to be checked.

    Returns:
        bool: True if the helper can be activated, False otherwise.
    """
    return player.coin >= helper.cost and mode in helper.allow_mode and helper.available
  
def show_menu_page_background(window:pygame.Surface):
    """
    Display the background image and title text on the menu page.

    Args:
        window (pygame.Surface): The pygame window.
    """
    window.fill(BEIGE)
    image = pygame.image.load("assets/image/Home page.png")
    menu_image = pygame.transform.smoothscale(image, (SCREEN_WIDTH, 1080))
    window.blit(menu_image, (0,0))
    
    font = pygame.font.Font("assets/font/one piece font.ttf", 100)
    text = font.render("ONE PIECE" , True , BLACK)
    text_width, text_height = text.get_rect().size
    window.blit(text, ((SCREEN_WIDTH-text_width)/2+20, 40))
    
    text = font.render("MAZE GAME" , True , BLACK)
    text_width, text_height = text.get_rect().size
    window.blit(text, ((SCREEN_WIDTH-text_width)/2+20, 140))
   
def generate_random_position(block_in_maze, pos_set:set):
    """
    Generate a random position for game elements in the maze.

    Args:
        block_in_maze (int): The number of blocks in the maze.
        pos_set (set): A set containing existing positions in the maze.

    Returns:
        tuple: A tuple representing the generated position.
    """
    global my_seed
    pos = (random.choice(range(block_in_maze)),random.choice(range(block_in_maze)),random.choice(range(CELL_IN_BLOCK)),random.choice(range(CELL_IN_BLOCK)))
        
    # avoid overlap with finish flag
    while pos in pos_set:
        my_seed += 1
        pos = (random.choice(range(block_in_maze)),random.choice(range(block_in_maze)),random.choice(range(CELL_IN_BLOCK)),random.choice(range(CELL_IN_BLOCK)))
    
    pos_set.add(pos)
    return pos

def create_item_dict(item_class, block_in_maze, counts_dict, pos_set):
    """
    Create a dictionary of items with randomly generated positions in the maze.

    Args:
        item_class: The class of the item to be created.
        block_in_maze (int): The number of blocks in the maze.
        counts_dict (dict): A dictionary containing the count of items for each block configuration.
        pos_set (set): A set containing existing positions in the maze.

    Returns:
        dict: A dictionary containing items with their positions as keys.
    """
    item_dict = {}
    count = counts_dict[block_in_maze]
    for i in range(count):
        pos = generate_random_position(block_in_maze, pos_set)
        block_number = pos[0] * block_in_maze + pos[1]
        key = (block_number, pos[2], pos[3])
        item_dict[key] = item_class(pos, block_in_maze, key)
    return item_dict

def check_show_item(player:Player, maze:Maze, item:Item):
    """
    Check if an item should be shown on the screen based on the player's position and maze configuration.

    Args:
        player (Player): The player object.
        maze (Maze): The maze object.
        item (Item): The item object.

    Returns:
        bool: True if the item should be shown, False otherwise.
    """
    if item.collect:
        return False
    if maze.cell_size == SMALL_MAZE_CELL_SIZE and item.visible == False:
        return False
    item_pos_x, item_pos_y = item.get_absolute_pos(maze)
    player_pos_x, player_pos_y = player.get_absolute_pos(maze)
    
    if maze.cell_size == SMALL_MAZE_CELL_SIZE:
        x_condition = player_pos_x-8*maze.cell_size <= item_pos_x <= player_pos_x+7*maze.cell_size 
        y_condition = player_pos_y-8*maze.cell_size <= item_pos_y <= player_pos_y+7*maze.cell_size
    else:
        x_condition = player_pos_x-4*maze.cell_size <= item_pos_x <= player_pos_x+3*maze.cell_size 
        y_condition = player_pos_y-4*maze.cell_size <= item_pos_y <= player_pos_y+3*maze.cell_size

    return x_condition and y_condition

def show_items_in_maze(item_dict:dict[tuple, Item], maze:Maze, window:pygame.Surface, player:Player, item_type:str):
    """
    Show items in the maze on the screen.

    Args:
        item_dict (dict): A dictionary containing items with their positions as keys.
        maze (Maze): The maze object.
        window (pygame.Surface): The pygame window.
        player (Player): The player object.
        item_type (str): The type of item to be shown.
    """
    item_image_path = f"assets/image/{item_type}.png"
    item_image = load_and_resize_image(item_image_path, (maze.cell_size, maze.cell_size))
    for item in item_dict.values():
        if check_show_item(player, maze, item):
            item.visible = True
            item_pos_x, item_pos_y = item.get_absolute_pos(maze)
            player_pos_x, player_pos_y = player.get_absolute_pos(maze)
            if maze.cell_size == SMALL_MAZE_CELL_SIZE:
                screen_middle_x = SMALL_SCREEN_POS[0]+(SMALL_SCREEN_WIDTH)/2
                screen_middle_y = SMALL_SCREEN_POS[1]+(SMALL_SCREEN_HEIGHT)/2
            else:
                screen_middle_x = LARGE_SCREEN_POS[0]+(VISIBLE_WIDTH)/2
                screen_middle_y = LARGE_SCREEN_POS[1]+(VISIBLE_HEIGHT)/2
            window.blit(item_image, (screen_middle_x+(item_pos_x-player_pos_x), screen_middle_y+(item_pos_y-player_pos_y)))

def show_items_in_middle_maze(window:pygame.Surface, middle_maze:Maze, item_dict:dict[tuple, Item], item_type):
    """
    Show items in the middle maze on the screen.

    Args:
        window (pygame.Surface): The pygame window.
        middle_maze (Maze): The middle maze object.
        item_dict (dict): A dictionary containing items with their positions as keys.
        item_type (str): The type of item to be shown.
    """
    item_image_path = f"assets/image/{item_type}.png"
    middle_image = load_and_resize_image(item_image_path, (middle_maze.cell_size, middle_maze.cell_size))
    for item in item_dict.values():
        if item.collect or item.visible == False:
            continue
        pos_x, pos_y = item.get_absolute_pos(middle_maze)
        window.blit(middle_image, (LARGE_SCREEN_POS[0] + pos_x, LARGE_SCREEN_POS[1] + pos_y))

def collect_item(item:Item, player:Player, item_type:str):
    """
    Collect an item and apply its effects on the player.

    Args:
        item (Item): The item object to be collected.
        player (Player): The player object.
        item_type (str): The type of the item.

    Returns:
        None
    """
    sound_effect = pygame.mixer.Sound(f"assets/sounds/{item_type}.mp3")
    sound_effect.play()
    item.collect = True
    if item_type == "coin":
        player.coin += 1
    elif item_type == "sword":
        player.attack += 1
    elif item_type == "meat":
        player.maximum_life += 10
        player.life += 20
        if player.life > player.maximum_life:
            player.life = player.maximum_life
    elif item_type == "coke":
        num = random.choice(range(4))
        if num == 0 and player.attack_dice.lower_bound < player.attack_dice.upper_bound:
            player.attack_dice.lower_bound += 1
        elif num == 1:
            player.attack_dice.upper_bound += 1
        elif num == 2 and player.defense_dice.lower_bound < player.defense_dice.upper_bound:
            player.defense_dice.lower_bound += 1
        elif num == 3:
            player.defense_dice.upper_bound += 1 
    elif item_type == "shield":
        player.defense += 1
    
def handle_item_interaction(player:Player, item_dict:dict[str, dict[tuple, Item]]):
    """
    Handle the interaction between the player and items in the maze.

    Args:
        player (Player): The player object.
        item_dict (dict): A dictionary containing items (dict) with their positions as keys.

    Returns:
        None
    """
    key = (player.block_number, player.cell_row, player.cell_col)
    for item_type, items in item_dict.items():
        if key in items.keys() and items[key].collect == False and item_type != "finish_flag": # finish flag will not handle here
            collect_item(items[key], player, item_type)
            
def handle_player_interaction(player, helper_dict, helper_rect_dict, item_dict, enemy_dict, window):
    """
    Handle player interaction with helpers, items, and enemies.

    Args:
        player (Player): The player object.
        helper_dict (dict): A dictionary containing helpers.
        helper_rect_dict (dict): A dictionary containing helper rectangles.
        item_dict (dict): A dictionary containing items with their positions as keys.
        enemy_dict (dict): A dictionary containing enemies with their positions as keys.
        window (pygame.Surface): The window surface.

    Returns:
        tuple: A tuple containing game state and result. The game state can be "game" or "game_over". 
        The result can be "win" or "lose".
    """
    player.step += 1
    update_player_on_step_change(player)
    
    # Activate helper skills if applicable
    for helper in helper_dict.values():
        if helper.activate and "game" in helper.allow_mode:
            use_skill_in_game_mode(player, window, helper)
            show_helper(window, helper_dict, player, "game")
    
    # Handle interaction with items
    handle_item_interaction(player, item_dict)
    
    # Check if the player is encountering an enemy
    key = (player.block_number, player.cell_row, player.cell_col)
    if key in enemy_dict.keys() and enemy_dict[key].defeated == False:
        battle(player, enemy_dict[key], window, helper_dict, helper_rect_dict)
        pygame.mixer.music.load('assets/sounds/Overtaken.mp3')
        pygame.mixer.music.play(-1)
        
    # Check if the player has reached the finish flag
    if key in item_dict["finish_flag"].keys():
        return ("game_over", "win")
    
    # Check if the player's life is depleted
    if player.life <= 0:
        return ("game_over", "lose")
    
    # If none of the game over conditions are met, continue the game
    return ("game", None) 

def play_game(window:pygame.Surface, block_in_maze):
    """
    Function to start and run the game.

    Args:
        window (pygame.Surface): The window surface for rendering.
        block_in_maze (int): The number of blocks in each row and column of the maze.

    Returns:
        tuple: A tuple containing the game state, player object, and result.
        The game state can be "quit" or "game_over".
        The result can be "win" or "lose".
    """
    # Initialize surfaces for different elements of the game
    maze_surface = pygame.Surface((VISIBLE_WIDTH+5, VISIBLE_HEIGHT+5))
    small_maze_surface = pygame.Surface((SMALL_SCREEN_WIDTH,SMALL_SCREEN_HEIGHT))
    middle_maze_surface = pygame.Surface((VISIBLE_WIDTH+5, VISIBLE_HEIGHT+5))
    exchange_block_button_surface = pygame.Surface((EXCHANGE_BLOCK_BUTTON_RECT_POS[2], EXCHANGE_BLOCK_BUTTON_RECT_POS[3]))
    input_box_surface = pygame.Surface((INPUT_BOX_RECT_POS[2], INPUT_BOX_RECT_POS[3]))
    
    # Play background music and set maze properties
    sound_effect = pygame.mixer.Sound('assets/sounds/set sail.ogg')
    sound_effect.play()
    pygame.mixer.music.load('assets/sounds/Overtaken.mp3')
    pygame.mixer.music.play(-1)
    maze = Maze(0, 0, block_in_maze, LARGE_MAZE_CELL_SIZE, 10)
    small_maze = Maze(0, 0, block_in_maze, SMALL_MAZE_CELL_SIZE, 3)
    middle_maze = Maze(0, 0, block_in_maze, VISIBLE_WIDTH/(block_in_maze*CELL_IN_BLOCK), 4 )
    
    # Generate the original mazes
    solution_path = maze.generate_maze(my_seed)
    small_maze.generate_maze(my_seed)
    middle_maze.generate_maze(my_seed)
    maze.show_block_number()
    
    # Save the solution path and solution image
    with open("./output/path.txt", "w") as fh:
        fh.write("block_row, block_col, cell_row, cell_col\n")
        for pos in solution_path:
            fh.write(str(pos)+'\n')
    # print(solution_path)
    save_image(maze, False, "./output/maze.jpg", solution_path)
    save_image(maze, True, "./output/solution.jpg", solution_path)
    
    # Randomize the maze and save it as randomize_maze.jpg
    maze.randomize(my_seed)
    save_image(maze, False, "./output/randomize_maze.jpg", solution_path)
    small_maze.randomize(my_seed)
    middle_maze.randomize(my_seed)
    
    # Initialize position set with start and end
    pos_set = set()
    start = solution_path[0]
    # start = solution_path[-2]
    end = solution_path[-1]
    pos_set.add(start)
    pos_set.add(end)
    
    # Set up item dictionaries, player, enemy, and helper objects
    player = Player(start, maze)
    coin_counts = {3: EASY_COIN_COUNT, 4: MEDIUM_COIN_COUNT, 5: HARD_COIN_COUNT}
    sword_counts = {3: EASY_SWORD_COUNT, 4: MEDIUM_SWORD_COUNT, 5: HARD_SWORD_COUNT}
    meat_counts = {3: EASY_MEAT_COUNT, 4: MEDIUM_MEAT_COUNT, 5: HARD_MEAT_COUNT}
    coke_counts = {3: EASY_COKE_COUNT, 4:MEDIUM_COKE_COUNT, 5: HARD_COKE_COUNT}
    shield_counts = {3: EASY_SHIELD_COUNT, 4:MEDIUM_SHIELD_COUNT, 5:HARD_SHIELD_COUNT}
    
    coin_dict = create_item_dict(Coin, block_in_maze, coin_counts, pos_set)
    sword_dict = create_item_dict(Sword, block_in_maze, sword_counts, pos_set)
    meat_dict = create_item_dict(Meat, block_in_maze, meat_counts, pos_set)
    coke_dict = create_item_dict(Coke, block_in_maze, coke_counts, pos_set)
    shield_dict = create_item_dict(Shield, block_in_maze, shield_counts, pos_set)
    
    finish_flag_dict = {}
    end = solution_path[-1]
    finish_flag_block_number = end[0] * block_in_maze + end[1]
    key = (finish_flag_block_number, end[2], end[3])
    finish_flag_dict[key] = FinishFlag(end, block_in_maze, key)
    
    item_dict = {
        "coin": coin_dict,
        "sword": sword_dict,
        "meat": meat_dict,
        "coke": coke_dict,
        "shield": shield_dict,
        "finish_flag": finish_flag_dict
    }
    
    if block_in_maze == 3:
        enemy_dict = create_easy_enemy(player, block_in_maze, pos_set)
    elif block_in_maze == 4:
        enemy_dict = create_medium_enemy(player, block_in_maze, pos_set)
    else:
        enemy_dict = create_hard_enemy(player, block_in_maze, pos_set)
    helper_dict = create_helper()
    helper_rect_dict = create_helper_rect_dict()
    
    
    # Initialize game window and display initial elements
    window.fill(BEIGE)
    image = load_and_resize_image("assets/image/Game Background.png", (SCREEN_WIDTH,SCREEN_HEIGHT)) 
    window.blit(image, (0,0))
    center_player_on_maze(player, maze)
    center_player_on_maze(player, small_maze)
    show_mazes_and_players_in_game_mode(window, maze, maze_surface, small_maze, small_maze_surface, "default")
    for item_type, item in item_dict.items():
        show_items_in_maze(item, maze, window, player, item_type)
        show_items_in_maze(item, small_maze, window, player, item_type)
    show_enemy_in_maze(enemy_dict, maze, window, player)
    show_enemy_in_maze(enemy_dict, small_maze, window, player)
    show_player_attribute_icon(window)
    show_player_attribute_value(window, player)
    show_helper(window, helper_dict, player, "game")
    show_helper_cost(window, helper_dict)

    # Show exchange block and input box
    exchange_block_rect = pygame.Rect(EXCHANGE_BLOCK_BUTTON_RECT_POS)
    input_box_rect = pygame.Rect(INPUT_BOX_RECT_POS)
    pygame.draw.rect(window, WHITE, input_box_rect)
    show_text_in_button(window, exchange_block_button_surface, "Exchange Block", (EXCHANGE_BLOCK_BUTTON_RECT_POS[0], EXCHANGE_BLOCK_BUTTON_RECT_POS[1]))

    # Show the initial screen
    pygame.display.update()
    pygame.image.save(window, "./output/Initial start.jpeg")
    
    # Print the block number after randomize to terminal
    maze.show_block_number()
    print(maze.get_block_number_list())
    
    
    cursor_state = "arrow"
    input_text = ""
    input_box_active = False
    mode = "game"
    running = True

    # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ("quit", player, "win")
            if event.type == pygame.KEYDOWN:
                # Handle key presses for movement and input
                if mode == "exchange_block":
                    if event.key == pygame.K_RETURN:
                        # Exchange the input block with current block
                        if input_text != "" and int(input_text) in range(maze.block_in_maze*maze.block_in_maze):
                            input_block_row, input_block_col = (int(input_text) // maze.block_in_maze, int(input_text) % maze.block_in_maze)
                            current_block_index = maze.get_block_number_index(player.block_number)
                            current_block_row, current_block_col = current_block_index[0], current_block_index[1]
                            maze.exchange_block((input_block_row, input_block_col), (current_block_row, current_block_col))
                            small_maze.exchange_block((input_block_row, input_block_col), (current_block_row, current_block_col))
                            middle_maze.exchange_block((input_block_row, input_block_col), (current_block_row, current_block_col))
                            
                            # Print the block number after exchange to the terminal
                            maze.show_block_number()
                            
                            # Update the screen
                            center_player_on_maze(player, small_maze)
                            center_player_on_maze(player, maze)
                            show_mazes_and_players_in_exchange_mode(window, middle_maze, middle_maze_surface, small_maze, small_maze_surface, player)
                            for item_type, item in item_dict.items():
                                show_items_in_middle_maze(window, middle_maze, item, item_type)
                                show_items_in_maze(item, small_maze, window, player, item_type)
                            show_enemy_in_middle_maze(window, middle_maze, enemy_dict)
                            show_enemy_in_maze(enemy_dict, small_maze, window, player)
                            
                        # Clear the input
                        input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        # Remove the last character from the input
                        input_text = input_text[:-1]
                    else:
                        # Append the pressed key to the input text
                        if event.unicode in ["0","1","2","3","4","5","6","7","8","9"]:
                            input_text += event.unicode
                            
                    show_text_in_button(window, input_box_surface, input_text, (INPUT_BOX_RECT_POS[0], INPUT_BOX_RECT_POS[1]))
                    pygame.display.update()
                    pygame.image.save(window, "./output/After Exchange.jpeg")
                    
                elif mode == "game":
                    # Initialize variables for player movement
                    validate_move_flag = False
                    direction = ""
                    game_state = "game"
                    result = None
                    
                    # Check which key is pressed and validate movement in that direction
                    if event.key == pygame.K_u:
                        if check_up_validate(maze, player):
                            validate_move_flag = True
                            direction = "up"
                            player.move_up(maze)
                            maze.move(0, maze.cell_size)
                            small_maze.move(0, small_maze.cell_size)
                    elif event.key == pygame.K_d:
                        if check_down_validate(maze, player):
                            validate_move_flag = True
                            direction = "down"
                            player.move_down(maze)
                            maze.move(0, -maze.cell_size)
                            small_maze.move(0, -small_maze.cell_size)
                    elif event.key == pygame.K_l:
                        if check_left_validate(maze, player):
                            validate_move_flag = True
                            direction = "left"
                            player.move_left(maze)
                            maze.move(maze.cell_size, 0)
                            small_maze.move(small_maze.cell_size, 0)
                    elif event.key == pygame.K_r:
                        if check_right_validate(maze, player):
                            validate_move_flag = True
                            direction = "right"
                            player.move_right(maze)
                            maze.move(-maze.cell_size, 0)
                            small_maze.move(-small_maze.cell_size, 0)
                    
                    # If movement is valid, handle player interaction
                    if validate_move_flag == True:
                        game_state, result = handle_player_interaction(player, helper_dict, helper_rect_dict, item_dict, enemy_dict, window) 
                        show_player_attribute_value(window, player)
                        
                        # Check if game is over after interaction
                        if game_state =="game_over":
                            return (game_state, player, result)
                        
                        # Load and display movement frames
                        frames_folder = f"./assets/image/move_{direction}"
                        frame_files = [f"{frames_folder}/frame_{i}.png" for i in range(1, 3)]
                        frames = [pygame.image.load(file) for file in frame_files]
                        
                        # Draw maze, items, enemies, and player in game mode
                        for image in frames:
                            show_mazes_and_players_in_game_mode(window,maze, maze_surface, small_maze, small_maze_surface, image)
                            for item_type, item in item_dict.items():
                                show_items_in_maze(item, maze, window, player, item_type)
                                show_items_in_maze(item, small_maze, window, player, item_type)
                            show_enemy_in_maze(enemy_dict, maze, window, player)
                            show_enemy_in_maze(enemy_dict, small_maze, window, player)
                            show_helper(window, helper_dict, player, "game")
                            pygame.display.update()
                            
            if event.type == pygame.MOUSEBUTTONDOWN:
                sound_effect = pygame.mixer.Sound('assets/sounds/mouse-click.mp3')
                sound_effect.play()
                
                # Handle mouse clicks for various interactions
                if exchange_block_rect.collidepoint(event.pos) and mode == "game":
                    # Switch to block exchange mode
                    mode = "exchange_block"
                    
                    # Update the screen
                    show_mazes_and_players_in_exchange_mode(window, middle_maze, middle_maze_surface, small_maze, small_maze_surface, player)
                    for item_type, item in item_dict.items():
                        show_items_in_middle_maze(window, middle_maze, item, item_type)
                        show_items_in_maze(item, small_maze, window, player, item_type)
                    show_enemy_in_middle_maze(window, middle_maze, enemy_dict)
                    show_enemy_in_maze(enemy_dict, small_maze, window, player)
                    show_text_in_button(window, exchange_block_button_surface, "Go Back", (EXCHANGE_BLOCK_BUTTON_RECT_POS[0], EXCHANGE_BLOCK_BUTTON_RECT_POS[1]))
                    pygame.display.update()
                    pygame.image.save(window, "./output/Exchange Mode.jpeg")
                    
                elif exchange_block_rect.collidepoint(event.pos) and mode == "exchange_block":
                    # Return to game mode from block exchange mode
                    mode = "game"
                    
                    # Update the screen
                    show_mazes_and_players_in_game_mode(window, maze, maze_surface, small_maze, small_maze_surface, "default")
                    show_enemy_in_maze(enemy_dict, maze, window, player)
                    show_enemy_in_maze(enemy_dict, small_maze, window, player)
                    for item_type, item in item_dict.items():
                        show_items_in_maze(item, maze, window, player, item_type)
                        show_items_in_maze(item, small_maze, window, player, item_type)
                    show_text_in_button(window, exchange_block_button_surface, "Exchange Block", (EXCHANGE_BLOCK_BUTTON_RECT_POS[0], EXCHANGE_BLOCK_BUTTON_RECT_POS[1]))
                    pygame.display.update()
                
                for name, helper in helper_dict.items():
                    if helper_rect_dict[name].collidepoint(event.pos) and check_helper_validate(player, mode, helper):
                        # Activate helper if clicked and conditions are met
                        helper.activate = True
                        helper.available = False
                        player.coin -= helper.cost
                        
                        # Update player attibute and show helper effect
                        show_player_attribute_value(window, player)
                        show_helper(window, helper_dict, player, "game")
                        show_helper_effect(window, helper)
                        
                        # Update the screen
                        show_mazes_and_players_in_game_mode(window,maze, maze_surface, small_maze, small_maze_surface, "default")
                        for item_type, item in item_dict.items():
                            show_items_in_maze(item, maze, window, player, item_type)
                            show_items_in_maze(item, small_maze, window, player, item_type)
                        show_enemy_in_maze(enemy_dict, maze, window, player)
                        show_enemy_in_maze(enemy_dict, small_maze, window, player)
                        pygame.display.update()

        # Change cursor appearance based on mouse position
        new_cursor_state = "arrow"
                    
        if exchange_block_rect.collidepoint(pygame.mouse.get_pos()):
            new_cursor_state = "hand"
            
        for helper, helper_rect in helper_rect_dict.items():
            if helper_rect.collidepoint(pygame.mouse.get_pos()) and check_helper_validate(player, mode, helper_dict[helper]):
                new_cursor_state = "hand"
        
        if new_cursor_state != cursor_state:
            if new_cursor_state == "hand":
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            cursor_state = new_cursor_state   
        

def show_menu(window:pygame.Surface):
    """
    Display the main menu screen and handle user interaction for starting a new game or quitting the game.

    Args:
        window (pygame.Surface): The surface of the game window.

    Returns:
        tuple: A tuple containing information about the user's choice.
               If the user chooses to quit, it returns ("quit", 3).
               If the user chooses to start a new game, it returns ("play", n), 
               where n represents the difficulty level chosen (3 for easy, 4 for medium, 5 for hard).
    """
    # Load background music and play it on loop
    pygame.mixer.music.load('assets/sounds/bgm_WeAre.wav')
    pygame.mixer.music.play(-1)
    
    # Define menu page buttons' rectangles
    new_game_rect = pygame.Rect(NEW_GAME_RECT_POS)
    quit_rect = pygame.Rect(QUIT_RECT_POS)
    
    # Define difficulty selection buttons' rectangles
    easy_rect = pygame.Rect(EASY_RECT_POS)
    medium_rect = pygame.Rect(MEDIUM_RECT_POS)
    hard_rect = pygame.Rect(HARD_RECT_POS)
    # pygame.draw.rect(window, RED, new_game_rect, 1)
    
    # Display menu page with buttons
    show_menu_page_background(window)
    font = pygame.font.Font("assets/font/one piece font.ttf", 80)
    
    # Render and display "NEW GAME" button
    text = font.render("NEW GAME" , True , WHITE)
    text_width, text_height = text.get_rect().size
    window.blit(text, ((SCREEN_WIDTH-text_width)/2+20, 750))
    
    # Render and display "QUIT" button
    text = font.render("QUIT" , True , WHITE)
    text_width, text_height = text.get_rect().size
    window.blit(text, ((SCREEN_WIDTH-text_width)/2+20, 830))
    
    # Update display
    pygame.display.update()
    
    running = True
    at_menu_page = True
    at_choosing_difficulty_page = False
    cursor_state = "arrow"
    
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    return ("quit", 3)
            if event.type == pygame.MOUSEBUTTONDOWN:
                sound_effect = pygame.mixer.Sound('assets/sounds/mouse-click.mp3')
                sound_effect.play()
                
                # Handling clicks on menu page
                if at_menu_page:
                    if new_game_rect.collidepoint(event.pos):
                        at_menu_page = False
                        at_choosing_difficulty_page = True
                        show_menu_page_background(window)
                        
                        # Draw difficulty selection buttons
                        pygame.draw.rect(window, WHITE, easy_rect, 2, border_radius=40)
                        pygame.draw.rect(window, WHITE, medium_rect, 2, border_radius=40)
                        pygame.draw.rect(window, WHITE, hard_rect, 2, border_radius=40)
                        
                        # Render and display difficulty selection buttons' text
                        font = pygame.font.Font("assets/font/one piece font.ttf", 80)
                        text = font.render("EASY" , True , WHITE)
                        text_width, text_height = text.get_rect().size
                        window.blit(text, ((SCREEN_WIDTH-text_width)/2+20, 650))
                        
                        text = font.render("MEDIUM" , True , WHITE)
                        text_width, text_height = text.get_rect().size
                        window.blit(text, ((SCREEN_WIDTH-text_width)/2+20, 750))
                        
                        text = font.render("HARD" , True , WHITE)
                        text_width, text_height = text.get_rect().size
                        window.blit(text, ((SCREEN_WIDTH-text_width)/2+20, 850))
                        
                        pygame.display.update()
                        
                    if quit_rect.collidepoint(event.pos):
                        return ("quit", 3)
                    
                # Handling clicks on difficulty selection page
                elif at_choosing_difficulty_page:
                    if easy_rect.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        return ("play", 3)
                    
                    if medium_rect.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        return ("play", 4)
                    
                    if hard_rect.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        return ("play", 5)
                    
        # Update cursor state based on mouse position
        new_cursor_state = "arrow"
        if at_menu_page:
            if new_game_rect.collidepoint(pygame.mouse.get_pos()) or quit_rect.collidepoint(pygame.mouse.get_pos()):
                new_cursor_state = "hand"
        
        if at_choosing_difficulty_page:
            if easy_rect.collidepoint(pygame.mouse.get_pos()) or medium_rect.collidepoint(pygame.mouse.get_pos())\
                or hard_rect.collidepoint(pygame.mouse.get_pos()):
                new_cursor_state = "hand"
        
        # Set cursor based on cursor state
        if new_cursor_state != cursor_state:
            if new_cursor_state == "hand":
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            cursor_state = new_cursor_state


def game_over(window:pygame.Surface, player:Player, result:str):
    """
    Display the game over screen based on the result of the game.

    Args:
        window (pygame.Surface): The surface of the game window.
        player (Player): The player object containing player's attributes and state.
        result (str): The result of the game, either "win" or "lose".

    Returns:
        str: A string indicating the next action after game over. 
             It can be "quit" to exit the game or "menu" to return to the main menu.
    """
    # Fill the window with beige color
    window.fill(BEIGE)
    
    cursor_state = "arrow"
    
    if result == "win":
        # Display winning screen
        image = load_and_resize_image("assets/image/brick_background.jpg", (SCREEN_WIDTH, 1080))
        window.blit(image, (0,0))
        image = load_and_resize_image("assets/image/wanted.png", (569, 800))
        window.blit(image, (450, 50))
        
        # Calculate final fame
        final_fame = player.fame + (player.attack * (player.attack_dice.upper_bound + player.attack_dice.lower_bound) + \
                                    player.defense*(player.defense_dice.lower_bound + player.defense_dice.upper_bound)) * 1000\
                                    - player.step * 100
                                    
        # Render and display final fame
        font = pygame.font.Font("assets/font/one piece font.ttf", 60)
        rect = pygame.Rect((550, 700, 335, 60))
        text = font.render(f"{final_fame}" , True , BLACK)
        text_rect = text.get_rect(center=rect.center)
        window.blit(text, text_rect)
        pygame.display.update()
        
        # Play victory music
        music_track = ["assets/sounds/pirate king.ogg","assets/sounds/Binks' Sake.mp3"]
        for idx, music in enumerate(music_track):
            pygame.mixer.music.load(music)
            pygame.mixer.music.play()
            if idx == 1:
                pygame.mixer.music.play(-1)
            else:
                while pygame.mixer.music.get_busy():
                    continue
    
    else:
        # Display losing screen
        music_track = ["assets/sounds/weak.mp3","assets/sounds/Mother Sea.mp3"]
        image = load_and_resize_image("assets/image/lose.jpg", (SCREEN_WIDTH, 1080))
        window.blit(image, (0,0))
        pygame.display.update()
        
        # Play losing music
        for idx, music in enumerate(music_track):
            pygame.mixer.music.load(music)
            pygame.mixer.music.play()
            if idx == 1:
                pygame.mixer.music.play(-1)
            else:
                while pygame.mixer.music.get_busy():
                    continue
    
    # Define buttons' rectangles
    new_game_rect = pygame.Rect((450, 870, 285, 80))
    quit_rect = pygame.Rect((745, 870, 275, 80))
    
    # Draw buttons
    pygame.draw.rect(window, WHITE, new_game_rect, width=2, border_radius=40)
    pygame.draw.rect(window, WHITE, quit_rect, width=2, border_radius=40)
    
    # Render and display text on buttons
    font = pygame.font.Font("assets/font/one piece font.ttf", 60)
    text = font.render("MENU" , True , WHITE)
    text_rect = text.get_rect(center=new_game_rect.center)
    window.blit(text, text_rect)
    
    text = font.render("QUIT" , True , WHITE)
    text_rect = text.get_rect(center=quit_rect.center)
    window.blit(text, text_rect)
    
    pygame.display.update()
    
    running = True
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                sound_effect = pygame.mixer.Sound('assets/sounds/mouse-click.mp3')
                sound_effect.play()
                if new_game_rect.collidepoint(event.pos):
                    time.sleep(1)
                    return "menu"
                if quit_rect.collidepoint(event.pos):
                        return "quit"

            new_cursor_state = "arrow"
            if new_game_rect.collidepoint(pygame.mouse.get_pos()) or quit_rect.collidepoint(pygame.mouse.get_pos()):
                new_cursor_state = "hand"
            
            # Update cursor state based on mouse position
            if new_cursor_state != cursor_state:
                if new_cursor_state == "hand":
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                cursor_state = new_cursor_state
