import pygame
import sys

from const import *
from game import Game


class Main:
    
    def __init__(self):
        pygame.init()
        # tạo cửa sổ với kích thước width height
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # tiêu đề của trò chơi
        pygame.display.set_caption("Chess")
        # tạo đối tượng game
        self.game = Game()
    
    def mainloop(self):
        
        game = self.game
        screen = self.screen
        
        while True:
            game.show_background(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # thoát khỏi pygame
                    pygame.quit()
                    # thoát chương trình
                    sys.exit()
            
            
            
            # cập nhật màn hình sau khi vẽ
            pygame.display.update()
    
main = Main()
main.mainloop()