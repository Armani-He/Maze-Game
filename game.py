import pygame
from variables import *
import game_play 

def main():
    pygame.init() # Initialize pygame
    
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Create game window
    game_state = "menu" # Initialize game state to "menu"
    block_number = 3
    
    while game_state != "quit": # Main game loop
        if game_state == "menu":    # Display menu
            game_state, block_number = game_play.show_menu(window)
        elif game_state == "play":  # Play the game
            game_state, player, result = game_play.play_game(window, block_number)
        elif game_state == "game_over": # Game over
            game_state = game_play.game_over(window, player, result)
            
    pygame.quit()
    
if __name__ == "__main__":
    main()