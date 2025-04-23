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
from pgn import PGNBuilder
from convert_move import convert_cs_move_to_py_move

import clr

import chess
import chess.engine

dll_path = os.path.join(os.path.dirname(__file__), "ChessLib2.dll")
clr.AddReference(dll_path)
from ChessLib import Search2, Board as CsBoard, Move as CsMove

class Game:

    def __init__(self):
        self.next_player = WHITE_PLAYER
        self.player_color = None # màu của người chơi
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
        self.ai_color = None
        
        self.engine = chess.engine.SimpleEngine.popen_uci(
            "C:/Users/Hoa/Downloads/stockfish-windows-x86-64-avx2/stockfish/stockfish-windows-x86-64-avx2.exe"
        )
        
        self.pgn = PGNBuilder()
        

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
            
    def display_choose_piece(self, screen):
        selecting = True
        while selecting:
            # Vẽ khung nền cho text 
            box_width, box_height = 500, 350
            box_rect = pygame.Rect(WIDTH // 2 - box_width // 2, HEIGHT // 2 - 150, box_width, box_height)
            self.draw_transparent_rect(screen, (50, 50, 50), box_rect, 180, border_radius=25) 
            pygame.draw.rect(screen, WHITE, box_rect, 5, border_radius=25)  

            # Lấy vị trí chuột
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            promotion_options = [("BLACK", -20), ("WHITE", 80)]
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
                            if option == "BLACK":
                                self.ai_color = WHITE_PLAYER
                                self.player_color = BLACK_PLAYER
                            elif option == "WHITE":
                                self.ai_color = BLACK_PLAYER
                                self.player_color = WHITE_PLAYER
                            selecting = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
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
                                
                            c = 0
                            # check is_checkmate
                            if self.is_checkmate():
                                winner = WHITE_WIN if self.next_player == WHITE_PLAYER else BLACK_WIN
                                self.paused = True
                                c = self.display_paused_game(screen, winner)
                                
                            # check draw
                            if self.is_draw():
                                winner = DRAW
                                self.paused = True
                                c = self.display_paused_game(screen, winner)
                                
                            # next turn
                            if c != RESTART:
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
                        
                    if event.key == pygame.K_d:
                        self.paused = True
                        c = self.display_paused_game(screen, DRAW)
                        if c != RESTART:
                            self.next_turn()
                        
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
        self.display_choose_piece(screen)
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
            if self.next_player == self.ai_color:
                # self.ai.ai_move(screen)
                fen = None
                if self.next_player == WHITE_PLAYER:
                    fen = self.board.to_fen(next_player='w')
                else:
                    fen = self.board.to_fen(next_player='b')
                print(fen)
                board = CsBoard()
                board.LoadPosition(fen)
                searcher = Search2(board)
                time = 1000
                cs_move = searcher.getBestMove(time)
                py_move = convert_cs_move_to_py_move(cs_move)
                flag = cs_move.MoveFlag
                initial_row = py_move.initial.row
                initial_col = py_move.initial.col
                initial_piece = self.board.squares[initial_row][initial_col].piece
                final_row = py_move.final.row
                final_col = py_move.final.col
                final_piece = self.board.squares[final_row][final_col].piece
                captured = final_piece
                initial_ai_move = Square(initial_row, initial_col, initial_piece)
                final_ai_move = Square(final_row, final_col, final_piece)
                ai_move = None
                if flag == 1: #enpassant
                    last_move = self.board.getLastestMove()
                    ai_move = Move(initial_ai_move, final_ai_move, enpassant_captured_piece_prev_row=last_move.initial.row, enpassant_captured_piece_prev_col=last_move.initial.col, enpassant_captured_piece_row=initial_row, enpassant_captured_piece_col=final_col)
                else:
                    ai_move = Move(initial_ai_move, final_ai_move)
                self.board.move(initial_piece, ai_move)
                
                # promotion
                if flag == 3:
                    self.board.squares[final_row][final_col].piece = Queen(self.ai_color)
                elif flag == 4:
                    self.board.squares[final_row][final_col].piece = Knight(self.ai_color)
                elif flag == 5:
                    self.board.squares[final_row][final_col].piece = Rook(self.ai_color)
                elif flag == 6:
                    self.board.squares[final_row][final_col].piece = Bishop(self.ai_color)
                
                
                if isinstance(initial_piece, King) and abs(initial_col - final_col) > 1:
                    self.hasCastled[initial_piece] = True  # Đánh dấu rằng quân Vua đã nhập thành

                # added
                is_capture = captured
                is_check = 0  # You need to implement this
                is_checkmate = self.is_checkmate()
                is_castling = isinstance(initial_piece, King) and abs(
                    final_col - initial_col) == 2

                self.pgn.add_move(
                    ai_move,
                    initial_piece,
                    is_capture=is_capture,
                    is_check=is_check,
                    is_checkmate=is_checkmate,
                    is_castling=is_castling
                )
                
                # sounds
                check_sound = CAPTURE if captured else MOVE
                if self.sound: self.play_sound(check_sound)
                # show methods
                self.show_bg(screen)
                self.show_last_move(screen)
                self.show_pieces(screen)
                
                c = 0
                # check is_checkmate
                if self.is_checkmate():
                    winner = WHITE_WIN if self.next_player == WHITE_PLAYER else BLACK_WIN
                    self.paused = True
                    c = self.display_paused_game(screen, winner)
                    
                # check draw
                if self.is_draw():
                    winner = DRAW
                    self.paused = True
                    c = self.display_paused_game(screen, winner)
                    
                # next turn
                if c != RESTART:
                    self.next_turn()

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
                                
                                check_promotion = list()
                                self.board.move(self.dragger.piece, move, promotion=check_promotion)
                                
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
                                
                                # check promotion
                                if len(check_promotion) > 0:
                                    self.display_promotion(piece, final, screen)
                                
                                c = 0
                                # check is_checkmate
                                if self.is_checkmate():
                                    winner = WHITE_WIN if self.next_player == WHITE_PLAYER else BLACK_WIN
                                    self.paused = True
                                    c = self.display_paused_game(screen, winner)
                                    
                                # check draw
                                if self.is_draw():
                                    winner = DRAW
                                    self.paused = True
                                    c = self.display_paused_game(screen, winner)
                                    
                                # next turn
                                if c != RESTART:
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
                            self.back()
                            self.back()
                            
                        if event.key == pygame.K_d:
                            self.paused = True
                            c = self.display_paused_game(screen, DRAW)
                            if c != RESTART:
                                self.next_turn()

                    # quit application
                    elif event.type == pygame.QUIT:
                        self.running = False
                        self.engine.quit()
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
                                return RESTART
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
        self.next_player = WHITE_PLAYER
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()
        self.paused = False
        self.running = True
        self.sound = True
        self.sound_rect = pygame.Rect(SOUND_RECT)
        # theo dõi nút đang được hover
        self.last_hover_button = None
        self.hasCastled = {WHITE_PIECE: False, BLACK_PIECE: False}
        
        # fifty-move rule
        self.count_fifty_move_rule = 0
        
        # ai
        self.ai = AIEngine(self.board, self)  # Khởi tạo AIEngine

        
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
        if self.count_fifty_move_rule >= 50:
            return True
        n = len(self.board.last_moves)
        if n >= 11:
            if self.board.last_moves[n-10] == self.board.last_moves[n-6] and \
                self.board.last_moves[n-6] == self.board.last_moves[n-2] and \
                self.board.last_moves[n-9] == self.board.last_moves[n-5] and \
                self.board.last_moves[n-5] == self.board.last_moves[n-1] and \
                self.board.last_moves[n-8] == self.board.last_moves[n-4] and \
                self.board.last_moves[n-7] == self.board.last_moves[n-3]:
                return True
        return False
