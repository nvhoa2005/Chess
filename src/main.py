import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):
        
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        
        game.play_background_sound()
        # show menu
        while game.menu:
            game.play_video(screen)
            # if game.sound:
            #     game.show_sound(screen, game.sound)
            #     game.unpause_sound()
            # else:
            #     game.show_sound(screen, game.sound)
            #     game.pause_sound()
            sound_rect = pygame.Rect(680, 10, 120, 110)
            
            # Vẽ khung nền cho text 
            box_width, box_height = 400, 350 
            box_rect = pygame.Rect(WIDTH // 2 - box_width // 2, HEIGHT // 2 - 150, box_width, box_height)
            game.draw_transparent_rect(screen, (50, 50, 50), box_rect, 180, border_radius=25) 
            pygame.draw.rect(screen, WHITE, box_rect, 5, border_radius=25)  

            # Hiển thị text
            title_text = game.config.start_menu_font.render("Select Mode", True, WHITE)
            title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
            screen.blit(title_text, title_rect)

            # Lấy vị trí chuột
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Tạo danh sách các nút chọn chế độ chơi
            button_rects = {}
            
            # Danh sách các tùy chọn chế độ chơi
            options = [("PVP", -60), ("AI", 40), ("Quit", 140)]

            for text, y_offset in options:
                is_hovered = False
                button_rect = game.draw_button(screen, text, (WIDTH // 2, HEIGHT // 2 + y_offset), 280, 80, game.config.start_menu_font, is_hovered)

                if button_rect.collidepoint(mouse_x, mouse_y):
                    if game.last_hover_button != text:  
                        if game.sound: game.play_sound("hover")
                        game.last_hover_button = text
                
                    button_rect = game.draw_button(screen, text, (WIDTH // 2, HEIGHT // 2 + y_offset), 280, 80, game.config.start_menu_font, hover=True)
                elif game.last_hover_button == text: 
                    game.last_hover_button = None

                button_rects[text] = button_rect

            pygame.display.update()

            # Xử lý sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game.sound: game.play_sound("click")
                    for text, button_rect in button_rects.items():
                        print(event.pos)
                        if button_rect.collidepoint(event.pos):
                            if text == "Player vs Player":
                                selected_mode = "pvp"
                            elif text == "Player vs AI":
                                selected_mode = "ai"
                            elif text == "Quit":
                                pygame.quit()
                                sys.exit()
                            game.menu = False  
                    if sound_rect.collidepoint(event.pos):
                        if game.sound: game.sound = False
                        else: game.sound = True

        while game.running:
            if game.sound: game.pause_sound()
            # show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            while game.paused:
                # if game.sound:
                #     game.show_sound(screen, game.sound)
                #     game.unpause_sound()
                # else:
                #     game.show_sound(screen, game.sound)
                #     game.pause_sound()
                # Hiển thị chữ "PAUSE"
                pause_text = game.config.paused_font.render("PAUSED", True, (200, 200, 200))
                pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
                screen.blit(pause_text, pause_rect)

                # Vẽ khung nền cho text 
                box_width, box_height = 400, 350 
                box_rect = pygame.Rect(WIDTH // 2 - box_width // 2, HEIGHT // 2 - 150, box_width, box_height)
                pygame.draw.rect(screen, (50, 50, 50), box_rect, border_radius=25) 
                pygame.draw.rect(screen, (255, 255, 255), box_rect, 5, border_radius=25)  

                # Lấy vị trí chuột
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Các nút menu
                options = [("Continue", -60), ("Restart", 40), ("Quit", 140)]
                button_rects = {}

                for text, y_offset in options:
                    button_rect = game.draw_button(screen, text, (WIDTH // 2, HEIGHT // 2 + y_offset), 280, 80, game.config.paused_options_font, False)
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        if game.last_hover_button != text: 
                            if game.sound: game.play_sound("hover")
                            game.last_hover_button = text
                        button_rect = game.draw_button(screen, text, (WIDTH // 2, HEIGHT // 2 + y_offset), 280, 80, game.config.paused_options_font, True)
                    else: 
                        if game.last_hover_button == text: 
                            game.last_hover_button = None
                    button_rects[text] = button_rect

                pygame.display.update()  # Cập nhật màn hình

                # Xử lý sự kiện
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if game.sound: game.play_sound("click")
                        for text, button_rect in button_rects.items():
                            if button_rect.collidepoint(event.pos):
                                if text == "Continue":
                                    game.paused = False
                                elif text == "Restart":
                                    game.reset()
                                    game = self.game
                                    board = self.game.board
                                    dragger = self.game.dragger
                                elif text == "Quit":
                                    game.running = False
                                    pygame.quit()
                                    sys.exit()
                        if sound_rect.collidepoint(event.pos):
                            if game.sound: game.sound = False
                            else: game.sound = True
                    elif event.type == pygame.QUIT:
                        game.running = False
                        pygame.quit()
                        sys.exit()


            
            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not game.paused:
                        dragger.update_mouse(event.pos)

                        clicked_row = dragger.mouseY // SQUARE_SIZE
                        clicked_col = dragger.mouseX // SQUARE_SIZE

                        # if clicked square has a piece ?
                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                            # valid piece (color) ?
                            if piece.color == game.next_player:
                                board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)
                                # show methods 
                                game.show_bg(screen)
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
                        # show methods
                        game.show_bg(screen)
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

                        # valid move ?
                        if board.valid_move(dragger.piece, move):
                            # normal capture
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)                            

                            # sounds
                            check_sound = "capture" if captured else "move"
                            if game.sound: game.play_sound(check_sound)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # next turn
                            game.next_turn()
                    
                    dragger.undrag_piece()
                
                # key press
                elif event.type == pygame.KEYDOWN:
                    
                    # changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()

                    # changing themes
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                        
                    # paused
                    if event.key == pygame.K_ESCAPE:
                        game.paused = not game.paused

                # quit application
                elif event.type == pygame.QUIT:
                    game.running = False
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()


main = Main()
main.mainloop()