from const import *
from square import Square
from piece import *
from move import Move


class Board:
    def __init__(self):
        self.squares = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.last_move = None
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")
        
    def move(self, piece, move):
        initial = move.initial
        final = move.final
        
        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        
        # move
        piece.moved = True
        
        # clear valid move
        piece.clear_moves()
        
        # set last move
        self.last_move = move
        
    
    def valid_move(self, piece, move):
        return move in piece.moves
    
    def calc_moves(self, piece, row, col):
        def pawn_moves():
            if piece.moved:
                steps = 1
            else:
                steps = 2
                
            start = row + piece.direction
            end = row + (piece.direction * (1+steps))
            for possible_move_row in range(start, end, piece.direction):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # create new move
                        move = Move(initial, final)
                        # append new valid move
                        piece.add_move(move)
                    else:
                        break
                else:
                    break
                
            possible_move_row = row + piece.direction
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create new move
                        move = Move(initial, final)
                        # append new valid move
                        piece.add_move(move)
        
        def knight_moves():
            possible_moves = [
                (row-2, col+1),
                (row+2, col-1),
                (row-2, col-1),
                (row+2, col+1),
                (row-1, col-2),
                (row-1, col+2),
                (row+1, col-2),
                (row+1, col+2)
            ]
            
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create new move
                        move = Move(initial, final)
                        # append new valid move
                        piece.add_move(move)
        
        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr
                
                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create new move
                        move = Move(initial, final)
                        
                        # empty
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # append new valid move
                            piece.add_move(move)
                        
                        # has enemy piece
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            piece.add_move(move)
                            break
                            
                        # has team piece
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                        
                        possible_move_row, possible_move_col = possible_move_row + row_incr, possible_move_col + col_incr 
                    else:
                        break
        
        def king_moves():
            possible_moves = [
                (row-1, col),
                (row+1, col),
                (row, col-1),
                (row, col+1),
                (row+1, col+1),
                (row+1, col-1),
                (row-1, col+1),
                (row-1, col-1)
            ]
            
            # normal moves
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create new move
                        move = Move(initial, final)
                        # append new valid move
                        piece.add_move(move)
                        
            # castling moves
            
            def check_castling_left():
                if self.squares[row][0].piece.moved: return False
                for i in range(1, col):
                    if(self.squares[row][i].has_piece()):
                        return False
                return True
            
            def check_castling_right():
                if self.squares[row][7].piece.moved: return False
                for i in range(col+1, 7):
                    if(self.squares[row][i].has_piece()):
                        return False
                return True
            
            if piece.moved == False:
                if check_castling_left():
                    # create squares of the new move
                    initial = Square(row, col)
                    final = Square(row, col-2)
                    # create new move
                    move = Move(initial, final)
                    # append new valid move
                    piece.add_move(move)
                if check_castling_right():
                    # create squares of the new move
                    initial = Square(row, col)
                    final = Square(row, col+2)
                    # create new move
                    move = Move(initial, final)
                    # append new valid move
                    piece.add_move(move)
        
        if isinstance(piece, Pawn):
            pawn_moves()
        
        elif isinstance(piece, Knight):
            knight_moves()
        
        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1)
            ])
        
        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1)
            ])
        
        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1),
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1)
            ])
        
        elif isinstance(piece, King):
            king_moves()
    
    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
    
    def _add_pieces(self, color):
        if color == "white":
            row_pawn, row_other = (6, 7)
        else:
            row_pawn, row_other = (1, 0)
            
        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
            
        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))
            
        # nights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
        
        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
        
        # queens
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))      
        
        # kings
        self.squares[row_other][4] = Square(row_other, 4, King(color))