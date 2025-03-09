import pygame

from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square

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
        # theo dõi nút đang được hover
        self.last_hover_button = None

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
                    
                    # all pieces except dragger piece
                    if piece is not self.dragger.piece:
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

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

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
        
    # Vẽ button
    def draw_button(self, screen, text, position, width, height, font, hover=False):
        # vị trí button
        rect = pygame.Rect(position[0] - width // 2, position[1] - height // 2, width, height)
        
        # Khi hover
        bg_color = (200, 200, 200) if hover else (120, 120, 120)
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