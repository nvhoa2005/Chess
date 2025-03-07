import pygame

from const import*

class Game:
    
    def __init__(self):
        pass

    def show_background(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200)
                else:
                    color = (119, 154, 88)
                    
                # vị trí góc trên của ô, chiều cao, chiều rộng ô
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                
                # vẽ ô lên màn hình
                pygame.draw.rect(surface, color, rect)