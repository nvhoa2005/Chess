import pygame
import sys

from const import *
from game import Game

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):
        
        screen = self.screen
        game = self.game
        game.play_background_sound()
        
        # display menu
        choice = game.display_menu(screen)

        # display game
        if choice == PVP:
            game.display_pvp_game(screen)
        elif choice == AI:
            game.display_ai_game(screen)
        elif choice == QUIT:
            game.running = False
            pygame.quit()
            sys.exit()
            

if __name__ == "__main__":
    main = Main()
    main.mainloop()