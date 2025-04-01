import pygame
import sys
import random

from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square
from move import Move
from piece import *
from ai_engine import AIEngine

class Game:

    def __init__(self):
        self.next_player = WHITE_PLAYER
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()
        self.paused = False
        self.running = True
        self.menu = True
        self.sound = True
        self.sound_rect = pygame.Rect(SOUND_RECT)
        # theo dõi nút đang được hover
        self.last_hover_button = None
        self.hasCastled = {WHITE_PIECE: False, BLACK_PIECE: False}
        
        # fifty-move rule
        self.count_fifty_move_rule = 0
        
        # ai
        self.ai = AIEngine(self.board, self)  # Khởi tạo AIEngine

    # blit methods
    def show_bg(self, surface):
        theme = self.config.theme
        
        for row in range(ROWS):
            for col in range(COLS):
                # color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # rect
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if col == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(str(ROWS-row), 1, color)
                    lbl_pos = (5, 5 + row * SQUARE_SIZE)
                    # blit
                    surface.blit(lbl, lbl_pos)

                # col coordinates
                if row == 7:
                    # color
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * SQUARE_SIZE + SQUARE_SIZE - 20, HEIGHT - 20)
                    # blit
                    surface.blit(lbl, lbl_pos)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    piece.set_texture(size=80)
                    img = pygame.image.load(piece.texture)
                    img_center = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                    piece.texture_rect = img.get_rect(center=img_center)
                    surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            # loop all valid moves
            for move in piece.moves:
                # color
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                # rect
                rect = (move.final.col * SQUARE_SIZE, move.final.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme
        lastestMove = self.board.getLastestMove()
        
        if lastestMove:
            initial = lastestMove.initial
            final = lastestMove.final

            for pos in [initial, final]:
                # color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                # rect
                rect = (pos.col * SQUARE_SIZE, pos.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            # color
            color = (180, 180, 180)
            # rect
            rect = (self.hovered_sqr.col * SQUARE_SIZE, self.hovered_sqr.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            # blit
            pygame.draw.rect(surface, color, rect, width=3)
            
    def show_sound(self, surface, status=True):
        if status:
            sound_on_img = pygame.image.load("assets/images/img/sound_on.png")
            sound_icon_rect = sound_on_img.get_rect(topright=(WIDTH-10, 20))
            surface.blit(sound_on_img, sound_icon_rect)
        else:
            sound_off_img = pygame.image.load("assets/images/img/sound_off.png")
            sound_icon_rect = sound_off_img.get_rect(topright=(WIDTH-10, 20))
            surface.blit(sound_off_img, sound_icon_rect)
            
    def display_menu(self, screen):
        while self.menu:
            self.play_video(screen)
            # if self.sound:
            #     self.show_sound(screen, self.sound)
            #     self.unpause_sound()
            # else:
            #     self.show_sound(screen, self.sound)
            #     self.pause_sound()
            
            # Vẽ khung nền cho text 
            box_width, box_height = 400, 350 
            box_rect = pygame.Rect(WIDTH // 2 - box_width // 2, HEIGHT // 2 - 150, box_width, box_height)
            self.draw_transparent_rect(screen, (50, 50, 50), box_rect, 180, border_radius=25) 
            pygame.draw.rect(screen, WHITE, box_rect, 5, border_radius=25)  

            # Hiển thị text
            title_text = self.config.start_menu_font.render(SELECT_MODE, True, WHITE)
            title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
            screen.blit(title_text, title_rect)

            # Lấy vị trí chuột
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Danh sách các nút chọn chế độ chơi
            button_rects = {}
            
            # Chế độ
            options = [("PVP", -60), ("AI", 40), ("Quit", 140)]

            for text, y_offset in options:
                is_hovered = False
                button_rect = self.draw_button(screen, text, (WIDTH // 2, HEIGHT // 2 + y_offset), 280, 80, self.config.start_menu_font, is_hovered)

                if button_rect.collidepoint(mouse_x, mouse_y):
                    if self.last_hover_button != text:  
                        if self.sound: self.play_sound(HOVER)
                        self.last_hover_button = text
                
                    button_rect = self.draw_button(screen, text, (WIDTH // 2, HEIGHT // 2 + y_offset), 280, 80, self.config.start_menu_font, hover=True)
                elif self.last_hover_button == text: 
                    self.last_hover_button = None

                button_rects[text] = button_rect

            pygame.display.update()

            # Xử lý sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound: self.play_sound(CLICK)
                    for text, button_rect in button_rects.items():
                        if button_rect.collidepoint(event.pos):
                            if text == "PVP":
                                self.display_pvp_game(screen)
                            elif text == "AI":
                                self.display_ai_game(screen)
                            elif text == "Quit":
                                self.running = False
                                pygame.quit()
                                sys.exit()
                            self.menu = False  
                    if self.sound_rect.collidepoint(event.pos):
                        if self.sound: self.sound = False
                        else: self.sound = True
            
    def display_pvp_game(self, screen):
        self.reset()
        while self.running:
            if self.sound: self.pause_sound()
            # show methods
            self.show_bg(screen)
            self.show_last_move(screen)
            self.show_moves(screen)
            self.show_pieces(screen)
            self.show_hover(screen)

            if self.paused:
                self.display_paused_game(screen, PAUSED_GAME)
            
            if self.dragger.dragging:
                self.dragger.update_blit(screen)

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.paused:
                        self.dragger.update_mouse(event.pos)

                        clicked_row = self.dragger.mouseY // SQUARE_SIZE
                        clicked_col = self.dragger.mouseX // SQUARE_SIZE

                        # if clicked square has a piece ?
                        if self.board.squares[clicked_row][clicked_col].has_piece():
                            piece = self.board.squares[clicked_row][clicked_col].piece
                            # valid piece (color) ?
                            if piece.color == self.next_player:
                                
                                # print("|| các nước đi được")
                                # for move in piece.moves:
                                #     init = move.initial
                                #     fi = move.final
                                #     print(init.row, init.col, "----", fi.row, fi.col)
                                # print("các nước đi được ||")
                                
                                # piece.clear_moves()
                                
                                # print("|| các nước đi được")
                                # for move in piece.moves:
                                #     init = move.initial
                                #     fi = move.final
                                #     print(init.row, init.col, "----", fi.row, fi.col)
                                # print("các nước đi được ||")
                                
                                self.board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                
                                # print("|| các nước đi được")
                                # for move in piece.moves:
                                #     init = move.initial
                                #     fi = move.final
                                #     print(init.row, init.col, "----", fi.row, fi.col)
                                # print("các nước đi được ||")
                                
                                self.dragger.save_initial(event.pos)
                                self.dragger.drag_piece(piece)
                                # show methods 
                                self.show_bg(screen)
                                self.show_last_move(screen)
                                self.show_moves(screen)
                                self.show_pieces(screen)
                
                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQUARE_SIZE
                    motion_col = event.pos[0] // SQUARE_SIZE

                    self.set_hover(motion_row, motion_col)

                    if self.dragger.dragging:
                        self.dragger.update_mouse(event.pos)
                        
                        # show methods
                        self.show_bg(screen)
                        self.show_last_move(screen)
                        self.show_moves(screen)
                        self.show_pieces(screen)
                        self.show_hover(screen)
                        self.dragger.update_blit(screen)
                
                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    if self.dragger.dragging:
                        self.dragger.update_mouse(event.pos)

                        released_row = self.dragger.mouseY // SQUARE_SIZE
                        released_col = self.dragger.mouseX // SQUARE_SIZE

                        # create possible move
                        initial_p = self.board.squares[self.dragger.initial_row][self.dragger.initial_col].piece
                        final_p = self.board.squares[released_row][released_col].piece
                        initial = Square(self.dragger.initial_row, self.dragger.initial_col, initial_p)
                        final = Square(released_row, released_col, final_p)
                        move = Move(initial, final)

                        # valid move ?
                        if self.board.valid_move(self.dragger.piece, move):
                            # normal capture
                            captured = self.board.squares[released_row][released_col].has_piece()

                            if isinstance(self.dragger.piece, Pawn) or self.board.squares[released_row][released_col].has_piece():
                                self.count_fifty_move_rule = 0
                            else:
                                self.count_fifty_move_rule += 1
                            print("Count fifty move rule: ", self.count_fifty_move_rule)
                            
                            check_promotion = list()
                            self.board.move(self.dragger.piece, move, promotion=check_promotion)
                            if isinstance(self.dragger.piece, King) and abs(initial.col - final.col) > 1:
                                self.hasCastled[self.dragger.piece] = True  # Đánh dấu rằng quân Vua đã nhập thành
                                
                            if move.enpassant_captured_piece_row is not None:
                                self.board.squares[move.enpassant_captured_piece_row][move.enpassant_captured_piece_col].piece = None
                            
                            # sounds
                            check_sound = CAPTURE if captured else MOVE
                            if self.sound: self.play_sound(check_sound)
                            # show methods
                            self.show_bg(screen)
                            self.show_last_move(screen)
                            self.show_pieces(screen)
                            
                            # check promotion
                            if len(check_promotion) > 0:
                                self.display_promotion(piece, final, screen)
                                
                            # check is_checkmate
                            if self.is_checkmate():
                                winner = WHITE_WIN if self.next_player == WHITE_PLAYER else BLACK_WIN
                                self.paused = True
                                self.display_paused_game(screen, winner)
                                
                            # check draw
                            if self.is_draw():
                                winner = DRAW
                                self.paused = True
                                self.display_paused_game(screen, winner)
                                
                            # next turn
                            self.next_turn()
                        # for row in range(ROWS):
                        #     for col in range(COLS):
                        #         if self.board.squares[row][col].has_piece():
                        #             tmp = self.board.squares[row][col].piece
                        #             print(tmp.name, tmp.color, end=" ")
                        #         else:
                        #             print("name color", end=" ")
                        #     print()
                    
                    self.dragger.undrag_piece()
                
                # key press
                elif event.type == pygame.KEYDOWN:
                    
                    # changing themes
                    if event.key == pygame.K_t:
                        self.change_theme()

                    # changing themes
                    if event.key == pygame.K_r:
                        self.reset()
                        
                    # paused
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                        
                    if event.key == pygame.K_b:
                        if self.board.numberOfLastMove > 0:
                            self.back()
                            self.show_bg(screen)
                            self.show_last_move(screen)
                            self.show_pieces(screen)
                            self.next_turn()

                # quit application
                elif event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()
            
    def display_ai_game(self, screen):
        self.reset()
        while self.running:
            if self.sound: self.pause_sound()
            # show methods
            self.show_bg(screen)
            self.show_last_move(screen)
            self.show_moves(screen)
            self.show_pieces(screen)
            self.show_hover(screen)

            if self.paused:
                self.display_paused_game(screen)
            
            if self.dragger.dragging:
                self.dragger.update_blit(screen)
                
            # ai move
            if self.next_player == BLACK_PLAYER:
                self.ai.ai_move(screen)

            else:
                for event in pygame.event.get():

                    # click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if not self.paused:
                            self.dragger.update_mouse(event.pos)

                            clicked_row = self.dragger.mouseY // SQUARE_SIZE
                            clicked_col = self.dragger.mouseX // SQUARE_SIZE

                            # if clicked square has a piece ?
                            if self.board.squares[clicked_row][clicked_col].has_piece():
                                piece = self.board.squares[clicked_row][clicked_col].piece
                                # valid piece (color) ?
                                if piece.color == self.next_player:
                                    
                                    # print("|| các nước đi được")
                                    # for move in piece.moves:
                                    #     init = move.initial
                                    #     fi = move.final
                                    #     print(init.row, init.col, "----", fi.row, fi.col)
                                    # print("các nước đi được ||")
                                    
                                    # piece.clear_moves()
                                    
                                    # print("|| các nước đi được")
                                    # for move in piece.moves:
                                    #     init = move.initial
                                    #     fi = move.final
                                    #     print(init.row, init.col, "----", fi.row, fi.col)
                                    # print("các nước đi được ||")
                                    
                                    self.board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                    
                                    # print("|| các nước đi được")
                                    # for move in piece.moves:
                                    #     init = move.initial
                                    #     fi = move.final
                                    #     print(init.row, init.col, "----", fi.row, fi.col)
                                    # print("các nước đi được ||")
                                    
                                    self.dragger.save_initial(event.pos)
                                    self.dragger.drag_piece(piece)
                                    # show methods 
                                    self.show_bg(screen)
                                    self.show_last_move(screen)
                                    self.show_moves(screen)
                                    self.show_pieces(screen)
                    
                    # mouse motion
                    elif event.type == pygame.MOUSEMOTION:
                        motion_row = event.pos[1] // SQUARE_SIZE
                        motion_col = event.pos[0] // SQUARE_SIZE

                        self.set_hover(motion_row, motion_col)

                        if self.dragger.dragging:
                            self.dragger.update_mouse(event.pos)
                            
                            # s = self.board.squares[motion_row][motion_col]
                            # if s.has_piece():
                            #     p = s.piece
                            #     print(s)
                            #     print(p.name, p.color)
                            #     print(s.isempty_or_enemy(self.dragger.piece.color))
                            
                            # show methods
                            self.show_bg(screen)
                            self.show_last_move(screen)
                            self.show_moves(screen)
                            self.show_pieces(screen)
                            self.show_hover(screen)
                            self.dragger.update_blit(screen)
                    
                    # click release
                    elif event.type == pygame.MOUSEBUTTONUP:
                        
                        if self.dragger.dragging:
                            self.dragger.update_mouse(event.pos)

                            released_row = self.dragger.mouseY // SQUARE_SIZE
                            released_col = self.dragger.mouseX // SQUARE_SIZE

                            # create possible move
                            initial_p = self.board.squares[self.dragger.initial_row][self.dragger.initial_col].piece
                            final_p = self.board.squares[released_row][released_col].piece
                            initial = Square(self.dragger.initial_row, self.dragger.initial_col, initial_p)
                            final = Square(released_row, released_col, final_p)
                            move = Move(initial, final)

                            # valid move ?
                            if self.board.valid_move(self.dragger.piece, move):
                                # normal capture
                                captured = self.board.squares[released_row][released_col].has_piece()
                                self.board.move(self.dragger.piece, move)
                                self.board.update_castling_rights(piece.color, piece, initial, final)
                                if isinstance(self.dragger.piece, King) and abs(initial.col - final.col) > 1:
                                    self.hasCastled[self.dragger.piece] = True  # Đánh dấu rằng quân Vua đã nhập thành

                                # sounds
                                check_sound = CAPTURE if captured else MOVE
                                if self.sound: self.play_sound(check_sound)
                                # show methods
                                self.show_bg(screen)
                                self.show_last_move(screen)
                                self.show_pieces(screen)
                                # check is_checkmate
                                if self.is_checkmate():
                                    winner = WHITE_WIN if self.next_player == WHITE_PLAYER else BLACK_WIN
                                    self.paused = True
                                    self.display_paused_game(screen, winner)
                                # next turn
                                self.next_turn()
                            # for row in range(ROWS):
                            #     for col in range(COLS):
                            #         if self.board.squares[row][col].has_piece():
                            #             tmp = self.board.squares[row][col].piece
                            #             print(tmp.name, tmp.color, end=" ")
                            #         else:
                            #             print("name color", end=" ")
                            #     print()
                        
                        self.dragger.undrag_piece()
                    
                    # key press
                    elif event.type == pygame.KEYDOWN:
                        
                        # changing themes
                        if event.key == pygame.K_t:
                            self.change_theme()

                        # changing themes
                        if event.key == pygame.K_r:
                            self.reset()
                            
                        # paused
                        if event.key == pygame.K_ESCAPE:
                            self.paused = not self.paused

                    # quit application
                    elif event.type == pygame.QUIT:
                        self.running = False
                        pygame.quit()
                        sys.exit()
                
                pygame.display.update()

    def display_paused_game(self, screen, type=PAUSED_GAME):
        while self.paused:
            if type == PAUSED_GAME:
                # Hiển thị chữ "PAUSE"
                pause_text = self.config.paused_font.render(PAUSED_TEXT, True, (200, 200, 200))
                pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
                screen.blit(pause_text, pause_rect)
            elif type == WHITE_WIN:
                # Hiển thị chữ "WHITE WIN"
                pause_text = self.config.paused_font.render(WHITE_WIN_TEXT, True, WHITE)
                pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
                screen.blit(pause_text, pause_rect)
            elif type == BLACK_WIN:
                # Hiển thị chữ "BLACK WIN"
                pause_text = self.config.paused_font.render(BLACK_WIN_TEXT, True, BLACK)
                pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
                screen.blit(pause_text, pause_rect)
            elif type == DRAW:
                # Hiển thị chữ "DRAW"
                pause_text = self.config.paused_font.render(DRAW_TEXT, True, BLACK)
                pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
                screen.blit(pause_text, pause_rect)

            # Vẽ khung nền cho text 
            box_width, box_height = 400, 350 
            box_rect = pygame.Rect(WIDTH // 2 - box_width // 2, HEIGHT // 2 - 150, box_width, box_height)
            pygame.draw.rect(screen, (50, 50, 50), box_rect, border_radius=25) 
            pygame.draw.rect(screen, WHITE, box_rect, 5, border_radius=25)  

            # Lấy vị trí chuột
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Các nút menu
            options = [("Continue", -60), ("Restart", 40), ("Quit", 140)]
            button_rects = {}

            for text, y_offset in options:
                if type == PAUSED_GAME:
                    button_rect = self.draw_button(screen, text, (WIDTH // 2, HEIGHT // 2 + y_offset), 280, 80, self.config.paused_options_font, False)
                else:
                    if text == "Continue":
                        button_rect = self.draw_button(screen, text, (WIDTH // 2, HEIGHT // 2 + y_offset), 280, 80, self.config.paused_options_font, False, BLACK_WIN)
                    else:
                        button_rect = self.draw_button(screen, text, (WIDTH // 2, HEIGHT // 2 + y_offset), 280, 80, self.config.paused_options_font, False)
                if button_rect.collidepoint(mouse_x, mouse_y):
                    if self.last_hover_button != text: 
                        if self.sound: self.play_sound(HOVER)
                        self.last_hover_button = text
                    button_rect = self.draw_button(screen, text, (WIDTH // 2, HEIGHT // 2 + y_offset), 280, 80, self.config.paused_options_font, True)
                else: 
                    if self.last_hover_button == text: 
                        self.last_hover_button = None
                button_rects[text] = button_rect

            pygame.display.update()  

            # Xử lý sự kiện
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound: self.play_sound(CLICK)
                    for text, button_rect in button_rects.items():
                        if button_rect.collidepoint(event.pos):
                            if text == "Continue":
                                if type == PAUSED_GAME:
                                    self.paused = False
                            elif text == "Restart":
                                self.paused = False
                                self.reset()
                            elif text == "Quit":
                                self.__init__()
                                self.play_background_sound()
                                self.display_menu(screen)
                    if self.sound_rect.collidepoint(event.pos):
                        if self.sound: self.sound = False
                        else: self.sound = True
                elif event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                    
    def display_promotion(self, piece, final, screen):
        selecting = True
        while selecting:
            # Vẽ khung nền cho text 
            box_width, box_height = 600, 450
            box_rect = pygame.Rect(WIDTH // 2 - box_width // 2, HEIGHT // 2 - 150, box_width, box_height)
            self.draw_transparent_rect(screen, (50, 50, 50), box_rect, 180, border_radius=25) 
            pygame.draw.rect(screen, WHITE, box_rect, 5, border_radius=25)  

            # Hiển thị text
            title_text = self.config.start_menu_font.render("Select", True, BLACK)
            title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
            screen.blit(title_text, title_rect)

            # Lấy vị trí chuột
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            promotion_options = [("Queen", -60), ("Rook", 40), ("Bishop", 140), ("Knight", 240)]
            option_rects = {}

            for text, y_offset in promotion_options:
                button_rect = self.draw_button(screen, text, (WIDTH // 2, HEIGHT // 2 + y_offset), 280, 80, self.config.start_menu_font, hover=False)
                if button_rect.collidepoint(mouse_x, mouse_y):
                    if self.last_hover_button != text:  
                        if self.sound: self.play_sound(HOVER)
                        self.last_hover_button = text
                
                    button_rect = self.draw_button(screen, text, (WIDTH // 2, HEIGHT // 2 + y_offset), 280, 80, self.config.start_menu_font, hover=True)
                elif self.last_hover_button == text: 
                    self.last_hover_button = None

                option_rects[text] = button_rect

            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound:
                        self.play_sound(CLICK)
                    for option, rect in option_rects.items():
                        if rect.collidepoint(event.pos):
                            if option == "Queen":
                                self.board.squares[final.row][final.col].piece = Queen(piece.color)
                            elif option == "Rook":
                                self.board.squares[final.row][final.col].piece = Rook(piece.color)
                            elif option == "Bishop":
                                self.board.squares[final.row][final.col].piece = Bishop(piece.color)
                            elif option == "Knight":
                                self.board.squares[final.row][final.col].piece = Knight(piece.color)
                            selecting = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    # other methods

    def next_turn(self):
        self.next_player = WHITE_PLAYER if self.next_player == BLACK_PLAYER else BLACK_PLAYER

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, event_type):
        if event_type == CAPTURE:
            self.config.capture_sound.play()
        elif event_type == MOVE:
            self.config.move_sound.play()
        elif event_type == CLICK:
            self.config.click_sound.play()
        elif event_type == HOVER:
            self.config.hover_sound.play()
            
    def play_background_sound(self):
        self.config.background_sound.load()
            
    def pause_sound(self):
        self.config.background_sound.pause()
        
    def unpause_sound(self):
        self.config.background_sound.unpause()
            
    def play_video(self, screen):
        self.config.background_video.play(screen)

    def reset(self):
        self.__init__()
        
    def back(self):
        move = self.board.getLastestMove()
        self.board.undo_move(move)
        
    # Vẽ button
    def draw_button(self, screen, text, position, width, height, font, hover=False, type=PAUSED_GAME):
        # vị trí button
        rect = pygame.Rect(position[0] - width // 2, position[1] - height // 2, width, height)
        
        # Khi hover
        if type == PAUSED_GAME:
            bg_color = (200, 200, 200) if hover else (120, 120, 120)
        else:
            bg_color = (80, 80, 80) if hover else (50, 50, 50)
        pygame.draw.rect(screen, bg_color, rect, border_radius=20)  
        pygame.draw.rect(screen, WHITE, rect, 5, border_radius=20) 

        # Render chữ
        text_surface = font.render(text, True, BLACK if hover else WHITE)
        text_rect = text_surface.get_rect(center=position)
        screen.blit(text_surface, text_rect)
        
        return rect
    
    # vẽ hình chữ nhật có độ trong suốt lên một surface khác
    def draw_transparent_rect(self, screen, color, rect, opacity, border_radius):
        # Tạo một Surface mới với cùng cỡ hình chữ nhật
        transparent_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        # Vẽ hình chữ nhật bo góc lên Surface
        pygame.draw.rect(transparent_surface, (*color, opacity), 
                        (0, 0, rect.width, rect.height), border_radius=border_radius)
        # Vẽ Surface lên màn hình chính
        screen.blit(transparent_surface, (rect.x, rect.y))

    def get_all_moves(self, color):
        """
        Lấy tất cả các nước đi hợp lệ cho màu cờ được chọn.
        """
        moves = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece.color == color:
                        self.board.calc_moves(piece, row, col)
                        for move in piece.moves:
                            moves.append((piece, move))
        return moves

    # chiếu hết
    def is_checkmate(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_enemy_piece(self.next_player):
                    piece = self.board.squares[row][col].piece
                    self.board.calc_moves(piece, row, col)
                    if len(piece.moves) != 0:
                        return False
        return True
    
    def is_draw(self):
        if self.count_fifty_move_rule == 50:
            return True
