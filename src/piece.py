import os
from const import *

class Piece:

    def __init__(self, name, color, value, sign=0, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == WHITE_PIECE else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = 0
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect
        self.sign = sign

    def set_texture(self, size=80):
        self.texture = os.path.join(
            f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []

class Pawn(Piece):

    def __init__(self, color):
        self.dir = -1 if color == WHITE_PIECE else 1
        super().__init__(PAWN_NAME, color, 1.0, 5)

class Knight(Piece):

    def __init__(self, color):
        super().__init__(KNIGHT_NAME, color, 100, 4)

class Bishop(Piece):

    def __init__(self, color):
        super().__init__(BISHOP_NAME, color, 300, 3)

class Rook(Piece):

    def __init__(self, color):
        super().__init__(ROOK_NAME, color, 350, 2)

class Queen(Piece):

    def __init__(self, color):
        super().__init__(QUEEN_NAME, color, 500, 1)

class King(Piece):

    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__(KING_NAME, color, 10000.0, 0)