import pygame
import sys

from const import *
from game import Game

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption(GAME_NAME)
        self.game = Game()

    def mainloop(self):
        screen = self.screen
        game = self.game
        game.play_background_sound()
        game.display_menu(screen)

if __name__ == "__main__":
    main = Main()
    main.mainloop()