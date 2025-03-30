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

class Game:

    def __init__(self):
        self.next_player = 'white'
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
        
        # fifty-move rule
        self.count_fifty_move_rule = 0

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
            title_text = self.config.start_menu_font.render("Select Mode", True, WHITE)
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
                        if self.sound: self.play_sound("hover")
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
                    if self.sound: self.play_sound("click")
                    for text, button_rect in button_rects.items():
                        if button_rect.collidepoint(event.pos):
                            if text == "PVP":
                                return PVP
                            elif text == "AI":
                                return AI
                            elif text == "Quit":
                                self.running = False
                                pygame.quit()
                                sys.exit()
                                return QUIT
                            self.menu = False  
                    if self.sound_rect.collidepoint(event.pos):
                        if self.sound: self.sound = False
                        else: self.sound = True
            
    def display_pvp_game(self, screen):
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
                        initial = Square(self.dragger.initial_row, self.dragger.initial_col)
                        final = Square(released_row, released_col)
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
                            
                            # sounds
                            check_sound = "capture" if captured else "move"
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
                                winner = WHITE_WIN if self.next_player == "white" else BLACK_WIN
                                self.paused = True
                                self.display_paused_game(screen, winner)
                                
                            # check draw
                            if self.is_draw():
                                winner = DRAW
                                self.paused = True
                                self.display_paused_game(screen, winner)
                                
                            # next turn
                            self.next_turn()
                            print("=======")
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
                            print(self.next_player)
                            print(self.board.numberOfLastMove)

                # quit application
                elif event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()
            
    def display_ai_game(self, screen):
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
            if self.next_player == "black":
                self.ai_move(screen)

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
                            initial = Square(self.dragger.initial_row, self.dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)

                            # valid move ?
                            if self.board.valid_move(self.dragger.piece, move):
                                # normal capture
                                captured = self.board.squares[released_row][released_col].has_piece()
                                self.board.move(self.dragger.piece, move)

                                # sounds
                                check_sound = "capture" if captured else "move"
                                if self.sound: self.play_sound(check_sound)
                                # show methods
                                self.show_bg(screen)
                                self.show_last_move(screen)
                                self.show_pieces(screen)
                                # check is_checkmate
                                if self.is_checkmate():
                                    winner = WHITE_WIN if self.next_player == "white" else BLACK_WIN
                                    self.paused = True
                                    self.display_paused_game(screen, winner)
                                # next turn
                                self.next_turn()
                                print("=======")
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
        while True:
            if type == PAUSED_GAME:
                # Hiển thị chữ "PAUSE"
                pause_text = self.config.paused_font.render("PAUSED", True, (200, 200, 200))
                pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
                screen.blit(pause_text, pause_rect)
            elif type == WHITE_WIN:
                # Hiển thị chữ "WHITE WIN"
                pause_text = self.config.paused_font.render("WHITE WIN", True, WHITE)
                pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
                screen.blit(pause_text, pause_rect)
            elif type == BLACK_WIN:
                # Hiển thị chữ "BLACK WIN"
                pause_text = self.config.paused_font.render("BLACK WIN", True, BLACK)
                pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
                screen.blit(pause_text, pause_rect)
            elif type == DRAW:
                # Hiển thị chữ "DRAW"
                pause_text = self.config.paused_font.render("DRAW", True, BLACK)
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
                        if self.sound: self.play_sound("hover")
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
                    if self.sound: self.play_sound("click")
                    for text, button_rect in button_rects.items():
                        if button_rect.collidepoint(event.pos):
                            if text == "Continue":
                                if type == PAUSED_GAME:
                                    self.paused = False
                            elif text == "Restart":
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
                        if self.sound: self.play_sound("hover")
                        self.last_hover_button = text
                
                    button_rect = self.draw_button(screen, text, (WIDTH // 2, HEIGHT // 2 + y_offset), 280, 80, self.config.start_menu_font, hover=True)
                elif self.last_hover_button == text: 
                    self.last_hover_button = None

                option_rects[text] = button_rect

            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound:
                        self.play_sound("click")
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
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, event_type):
        if event_type == "capture":
            self.config.capture_sound.play()
        elif event_type == "move":
            self.config.move_sound.play()
        elif event_type == "click":
            self.config.click_sound.play()
        elif event_type == "hover":
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
        
        
    # =====================AI=======================
        
    def evaluate_board(self):
        """
        Đánh giá bàn cờ dựa trên giá trị quân cờ, vị trí và chiến thuật.
        """
        value = 0
        center_squares = {(3, 3), (3, 4), (4, 3), (4, 4)}  # Trung tâm bàn cờ
        piece_square_table = {
            "pawn": [
                0, 1, 2, 4, 5, 4, 2, 1,
                0, 1, 2, 3, 4, 3, 2, 1,
                0, 0, 1, 2, 3, 2, 1, 0,
                0, 0, 0, 1, 2, 1, 0, 0,
                0, 0, 0, 1, 2, 1, 0, 0,
                0, 0, 1, 2, 3, 2, 1, 0,
                0, 1, 2, 3, 4, 3, 2, 1,
                0, 1, 2, 4, 5, 4, 2, 1
            ],
            "knight": [
                -5, -3, 0, 0, 0, 0, -3, -5,
                -3, 0, 3, 4, 4, 3, 0, -3,
                0, 3, 5, 6, 6, 5, 3, 0,
                0, 4, 6, 7, 7, 6, 4, 0,
                0, 4, 6, 7, 7, 6, 4, 0,
                0, 3, 5, 6, 6, 5, 3, 0,
                -3, 0, 3, 4, 4, 3, 0, -3,
                -5, -3, 0, 0, 0, 0, -3, -5
            ],
            "bishop": [
                -2, -1, 0, 0, 0, 0, -1, -2,
                -1, 2, 3, 3, 3, 3, 2, -1,
                0, 3, 4, 5, 5, 4, 3, 0,
                0, 3, 5, 6, 6, 5, 3, 0,
                0, 3, 5, 6, 6, 5, 3, 0,
                0, 3, 4, 5, 5, 4, 3, 0,
                -1, 2, 3, 3, 3, 3, 2, -1,
                -2, -1, 0, 0, 0, 0, -1, -2
            ],
            "rook": [
                0, 0, 1, 2, 2, 1, 0, 0,
                -1, 0, 0, 0, 0, 0, 0, -1,
                -1, 0, 0, 0, 0, 0, 0, -1,
                -1, 0, 0, 0, 0, 0, 0, -1,
                -1, 0, 0, 0, 0, 0, 0, -1,
                -1, 0, 0, 0, 0, 0, 0, -1,
                1, 2, 2, 2, 2, 2, 2, 1,
                0, 0, 1, 2, 2, 1, 0, 0
            ],
            "queen": [
                -2, -1, 0, 1, 1, 0, -1, -2,
                -1, 0, 1, 1, 1, 1, 0, -1,
                0, 1, 1, 1, 1, 1, 1, 0,
                1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1,
                0, 1, 1, 1, 1, 1, 1, 0,
                -1, 0, 1, 1, 1, 1, 0, -1,
                -2, -1, 0, 1, 1, 0, -1, -2
            ],
            "king": [
                5, 5, 5, -5, -5, 5, 5, 5,
                3, 3, 3, -5, -5, 3, 3, 3,
                1, 1, 0, -5, -5, 0, 1, 1,
                0, 0, -5, -10, -10, -5, 0, 0,
                0, 0, -5, -10, -10, -5, 0, 0,
                1, 1, 0, -5, -5, 0, 1, 1,
                3, 3, 3, -5, -5, 3, 3, 3,
                5, 5, 5, -5, -5, 5, 5, 5
            ]
        }
        
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    base_value = piece.value
                    position_value = piece_square_table.get(piece.name, [0] * 64)[row * 8 + col] * 0.2  # Giảm trọng số vị trí
                    center_bonus = 2 if (row, col) in center_squares else 0
                    value += base_value + position_value + center_bonus if piece.color == "white" else - (base_value + position_value + center_bonus)
        return value

    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        """
        Cải tiến Alpha-Beta Pruning để tối ưu AI.
        """
        if depth == 0 or self.is_checkmate():
            return self.evaluate_board()
        
        moves = self.get_all_moves("black" if maximizing_player else "white")
        
        # Ưu tiên nước đi ăn quân
        moves.sort(key=lambda x: (x[1].final.piece.value if x[1].final.piece else 0), reverse=True)
        
        if maximizing_player:
            max_eval = float('-inf')
            for piece, move in moves:
                self.board.move(piece, move)
                eval = self.alpha_beta(depth - 1, alpha, beta, False)
                self.board.undo_move(move)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for piece, move in moves:
                self.board.move(piece, move)
                eval = self.alpha_beta(depth - 1, alpha, beta, True)
                self.board.undo_move(move)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

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

    def best_move(self, depth):
        """
        Cải thiện chọn nước đi tốt nhất dựa trên Alpha-Beta Pruning.
        """
        best_moves = []
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        moves = self.get_all_moves("black")
        moves.sort(key=lambda x: x[1].final.piece.value if x[1].final.piece else 0, reverse=True)  # Ưu tiên ăn quân
        
        for piece, move in moves:
            self.board.move(piece, move)
            move_value = self.alpha_beta(depth - 1, alpha, beta, False)
            self.board.undo_move(move)
            
            if move_value > best_value:
                best_value = move_value
                best_moves = [(piece, move)]
            elif move_value == best_value:
                best_moves.append((piece, move))
        
        return random.choice(best_moves) if best_moves else None

    def ai_move(self, screen):
        """
        Máy tính chọn nước đi tốt nhất hoặc kết thúc game nếu không có nước đi hợp lệ.
        """
        best_move = self.best_move(2)  # Độ sâu 3
        print("pass")
        if best_move:
            piece, move = best_move
            self.board.move(piece, move)
            self.show_bg(screen)
            self.show_last_move(screen)
            self.show_pieces(screen)
            self.next_turn()
        else:
            # Kiểm tra nếu AI bị chiếu hết hoặc hòa
            if self.is_checkmate():
                print("Checkmate! Người chơi thắng!")
            else:
                print("AI không thể di chuyển, ván cờ kết thúc.")
         
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
