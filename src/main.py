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
        dragger = self.game.dragger
        board = self.game.board
        
        while True:
            # show bàn cờ
            game.show_background(screen)
            # show các quân cờ
            game.show_pieces(screen)
            
            if dragger.dragging:
                dragger.update_blit(screen)
            
            for event in pygame.event.get():
                
                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    
                    clicked_row = dragger.mouseY // SQUARE_SIZE
                    clicked_col = dragger.mouseX // SQUARE_SIZE
                    
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)
                
                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        
                        # mỗi lần di chuyển vẽ lại toàn bộ bàn cờ để tránh lỗi bóng ma
                        game.show_background(screen)
                        game.show_pieces(screen)
                        
                        dragger.update_blit(screen)
                
                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.undrag_piece()
                
                # quit
                elif event.type == pygame.QUIT:
                    # thoát khỏi pygame
                    pygame.quit()
                    # thoát chương trình
                    sys.exit()
            
            
            
            # cập nhật màn hình sau khi vẽ
            pygame.display.update()
    
main = Main()
main.mainloop()