import pygame

from const import*
from board import Board
from dragger import Dragger

class Game:
    
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()

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
                
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    if piece is not self.dragger.piece:
                        # trả về kích thước ban đầu
                        piece.set_texture(size=80)
                        # tải ảnh của quân cờ từ đường dẫn
                        img = pygame.image.load(piece.texture)
                        # tính toán vị trí trung tâm mà quân cờ được đặt
                        img_center = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                        # lấy hình chữ nhật bao quanh ảnh và căn chỉnh hình chữ nhật tại trung tâm
                        piece.texture_rect = img.get_rect(center=img_center)
                        # vẽ ảnh của quân cờ lên bề mặt tại vị trí piece.texture_rect
                        surface.blit(img, piece.texture_rect)