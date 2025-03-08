import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move

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
            # show bước cuối cùng
            game.show_last_move(screen)
            # show các hướng đi hợp lệ
            game.show_moves(screen)
            # show các quân cờ
            game.show_pieces(screen)
            # show hover
            game.show_hover(screen)
            
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
                        # valid piece color
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            
                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                
                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQUARE_SIZE
                    motion_col = event.pos[0] // SQUARE_SIZE
                    game.set_hover(motion_row, motion_col)
                    
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # mỗi lần di chuyển vẽ lại toàn bộ bàn cờ để tránh lỗi bóng ma
                        game.show_background(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        
                        dragger.update_blit(screen)
                
                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // SQUARE_SIZE
                        released_col = dragger.mouseX // SQUARE_SIZE
                        
                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)
                        
                        if board.valid_move(dragger.piece, move):
                            board.move(dragger.piece, move)
                            # show methods
                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # next turn
                            game.next_turn()
                    
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