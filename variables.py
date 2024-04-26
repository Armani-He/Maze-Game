import random

SCREEN_WIDTH = 1540
SCREEN_HEIGHT = 1190
VISIBLE_WIDTH = 725
VISIBLE_HEIGHT = 725
LARGE_SCREEN_POS = (340, 190)
SMALL_SCREEN_WIDTH = 240
SMALL_SCREEN_HEIGHT = 240
SMALL_SCREEN_POS = (1110, 190)

CELL_IN_BLOCK = 8
LARGE_MAZE_CELL_SIZE = 90
SMALL_MAZE_CELL_SIZE = 15

LEFT, RIGHT, UP, DOWN = (0,-1), (0,1), (-1,0), (1,0)
DIRECTION = [LEFT, RIGHT, UP, DOWN]

WHITE = (255,255,255)
RED = (255, 0, 0)
LIGHT_GRAY = (211,211,211)
BEIGE = (245,245,220)
LIGHT_BROWN = (238,211,178)
DARK_BROWN = (105, 81, 67)
BLACK = (0,0,0)

EXCHANGE_BLOCK_BUTTON_RECT_POS = (1110, 457, 240, 50)
INPUT_BOX_RECT_POS = (1110, 520, 240, 50)
NEW_GAME_RECT_POS = (620, 750, 330, 80)
QUIT_RECT_POS = (620, 830, 330, 80)
EASY_RECT_POS = (620, 655, 330, 80)
MEDIUM_RECT_POS = (620, 755, 330, 80)
HARD_RECT_POS = (620, 855, 330, 80)

PLAYER_INFORMATION_IMAGE_SIZE = 30
HELPER_PORTRAIT_SIZE = 75
HELPER_COIN_SIZE = 15
BATTLE_PLAYER_IMAGE_SIZE = 150
TURN_ICON_IMAGE_SIZE = 60
PLAYER_INFORMATION_POS = (1110, 597)
PLAYER_INFORMATION_BATTLE_POS = (740, 760)
ENEMY_INFORMATION_POS = (400, 760)
HELPER_PORTRAIT_POS = (1110, 730)

PLAYER_INFORMATION_TEXT_RECT_POS = (1140, 597, 90, 30)
PLAYER_INFORMATION_TEXT_BATTLE_RECT_POS = (770, 760, 90, 30)
ENEMY_INFORMATION_TEXT_RECT_POS = (430, 760, 90, 30) 
PLAYER_DAMAGE_RECT_POS = (430, 730, 90, 30)
ENEMY_DAMAGE_RECT_POS = (770, 730, 90, 30)
HELPER_RECT_POS = (1110, 805, 65, 15)

PLAYER_ATTACK_POS_LIST = [(720, 600),(640, 600), (580, 600)]
ENEMY_ATTACK_POS_LIST = [(540, 600), (620, 600), (700, 600)]

EASY_COIN_COUNT = 50
MEDIUM_COIN_COUNT = 100
HARD_COIN_COUNT = 150
EASY_SWORD_COUNT = 8
MEDIUM_SWORD_COUNT = 15
HARD_SWORD_COUNT = 24 
EASY_MEAT_COUNT = 8
MEDIUM_MEAT_COUNT = 15
HARD_MEAT_COUNT = 24
STEP_COUNT = 30
EASY_COKE_COUNT = 5
MEDIUM_COKE_COUNT = 10
HARD_COKE_COUNT = 15
EASY_SHIELD_COUNT = 6
MEDIUM_SHIELD_COUNT = 10
HARD_SHIELD_COUNT = 15

ICON_LIST = ["heart", "attack", "defense", "step", "coin", "attack_dice", "defense_dice", "fame"]
ENEMY_ICON_LIST = ["heart", "attack", "defense", "fame", "attack_dice", "defense_dice"]
HELPER_LIST = ["Zoro", "Sanji", "Nami", "Usopp", "Chopper", "Brook"]
EASY_ENEMY_LIST = ["BUGGY", "Kuro", "Krieg", "Arlong"]
MEDIUM_ENEMY_LIST = ["BUGGY", "Kuro", "Krieg", "Arlong", "Crocodile", "Lucci", "Moria"]
HARD_ENEMY_LIST = ["BUGGY", "Kuro", "Krieg", "Arlong", "Crocodile", "Lucci", "Moria", "Magellan", "Katakuri", "Blackbeard"]
DELAY_TIME = 50
SKILL_EXECUTION_TIME_LIST = ["right_away", "before_attack", "after_attack", "before_defense", "after_defense"]


# my_seed = random.randint(0, 1000)
my_seed=42
random.seed(my_seed)