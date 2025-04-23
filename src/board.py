from const import *
from square import Square
from piece import *
from move import Move
import copy

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_moves = []
        self.numberOfLastMove = 0
        self._create()
        self._add_pieces(WHITE_PIECE)
        self._add_pieces(BLACK_PIECE)
        self.castling = {WHITE_PIECE: 0b11, BLACK_PIECE: 0b11}  # Quyền nhập thành (both kingside & queenside)
        self.hasCastled = {WHITE_PIECE: False, BLACK_PIECE: False}  # Trạng thái nhập thành của cả hai bên

    def getLastestMove(self):
        if self.numberOfLastMove > 0 and len(self.last_moves) > 0:
            return self.last_moves[-1]  
        return None

    def add_lastMove(self, move):
        self.last_moves.append(move)
        self.numberOfLastMove = len(self.last_moves)
        
    def delete_nearestMove(self):
        self.numberOfLastMove -=1
        self.last_moves.pop()

    def move(self, piece, move, testing=False, promotion=None):
        initial = move.initial
        final = move.final

        # Lưu quân cờ bị ăn (nếu có)
        move.captured_piece = self.squares[final.row][final.col].piece
        
        if move.enpassant_captured_piece_row is not None:
            move.captured_piece = self.squares[move.enpassant_captured_piece_row][move.enpassant_captured_piece_col].piece
            self.squares[move.enpassant_captured_piece_row][move.enpassant_captured_piece_col].piece = None

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        # if isinstance(piece, Rook):
        #     print(initial.row, initial.col, "----", final.row, final.col)
        self.squares[final.row][final.col].piece = piece

        if isinstance(piece, Pawn):
            if promotion is not None and self.check_promotion(final):
                promotion.append(1)
            
        # king castling
        if isinstance(piece, King):
            if not piece.moved and self.check_castling(initial, final) and not testing:
                diff = final.col - initial.col
                initR_p = None
                mR = None
                if diff < 0:
                    initR_p = self.squares[initial.row][0].piece
                    finalR_p = self.squares[initial.row][3].piece
                    initR = Square(initial.row, 0, initR_p)
                    finalR = Square(initial.row, 3, finalR_p)
                    mR = Move(initR, finalR)
                else:
                    initR_p = self.squares[initial.row][7].piece
                    finalR_p = self.squares[initial.row][5].piece
                    initR = Square(initial.row, 7, initR_p)
                    finalR = Square(initial.row, 5, finalR_p)
                    mR = Move(initR, finalR)
                initR_p.add_move(mR)
                if initR_p.moves:  # Kiểm tra nếu danh sách moves không rỗng
                    self.move(initR_p, mR)
                else:
                    print("No moves available for the rook.")

        # move
        piece.moved +=1

        # clear valid moves
        piece.clear_moves()

        # set last move
        if not testing:
            self.add_lastMove(move)

    def valid_move(self, piece, move):
        for m in piece.moves:
            if move == m and m.enpassant_captured_piece_row is not None:
                move.enpassant_captured_piece_prev_row = m.enpassant_captured_piece_prev_row
                move.enpassant_captured_piece_prev_col = m.enpassant_captured_piece_prev_col
                move.enpassant_captured_piece_row = m.enpassant_captured_piece_row
                move.enpassant_captured_piece_col = m.enpassant_captured_piece_col
                return 2
            elif move == m:
                return 1
        return 0
        

    def check_promotion(self, final):
        if final.row == 0 or final.row == 7:
            return True

    def check_castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)
        
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            del temp_piece
                            del temp_board
                            return True
        return False

    def calc_moves(self, piece, row, col, bool=True):
        '''
            Calculate all the possible (valid) moves of an specific piece on a specific position
        '''
        piece.clear_moves()
        
        def pawn_moves():
            # steps
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        # create initial and final move squares
                        initial_p = self.squares[row][col].piece
                        final_p = self.squares[possible_move_row][col].piece
                        initial = Square(row, col, initial_p)
                        final = Square(possible_move_row, col, final_p)
                        # create a new move
                        move = Move(initial, final)

                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)
                    # blocked
                    else: break
                # not in range
                else: break

            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # create initial and final move squares
                        initial_p1 = self.squares[row][col].piece
                        final_p1 = self.squares[possible_move_row][possible_move_col].piece
                        initial = Square(row, col, initial_p1)
                        final = Square(possible_move_row, possible_move_col, final_p1)
                        # create a new move
                        move = Move(initial, final)
                        
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)
                            
            # en passant
            last_move = self.getLastestMove()
            if last_move:
                last_piece = last_move.initial.piece
                if isinstance(last_piece, Pawn):
                    if abs(last_move.final.row - last_move.initial.row) == 2:
                        if last_move.final.row == row:
                            side_col = last_move.final.col
                            if Square.in_range(row, side_col):
                                side_square = self.squares[row][side_col]
                                if side_square.has_enemy_piece(piece.color):
                                    if isinstance(side_square.piece, Pawn):
                                        # create en passant move
                                        initial_p2 = self.squares[row][col].piece
                                        final_p2 = self.squares[row + piece.dir][side_col].piece
                                        initial = Square(row, col, initial_p2)
                                        final = Square(row + piece.dir, side_col, final_p2)
                                        move = Move(initial, final, enpassant_captured_piece_prev_row=last_move.initial.row, enpassant_captured_piece_prev_col=last_move.initial.col, enpassant_captured_piece_row=row, enpassant_captured_piece_col=side_col)
                                        
                                        if bool:
                                            if not self.in_check(piece, move):
                                                piece.add_move(move)
                                        else:
                                            piece.add_move(move)

        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create squares of the new move
                        initial_p3 = self.squares[row][col].piece
                        final_p3 = self.squares[possible_move_row][possible_move_col].piece
                        initial = Square(row, col, initial_p3)
                        final = Square(possible_move_row, possible_move_col, final_p3)
                        # create new move
                        move = Move(initial, final)
                        
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                # print("|| Nước được thêm")
                                # print(initial.row, initial.col, "----", final.row, final.col)
                                # print("Nước được thêm ||")
                                piece.add_move(move)
                        else:
                            # append new move
                            # print("|| Nước được thêm")
                            # print(initial.row, initial.col, "----", final.row, final.col)
                            # print("Nước được thêm ||")
                            piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # create squares of the possible new move
                        initial_p4 = self.squares[row][col].piece
                        final_p4 = self.squares[possible_move_row][possible_move_col].piece
                        initial = Square(row, col, initial_p4)
                        final = Square(possible_move_row, possible_move_col, final_p4)
                        # create a possible new move
                        move = Move(initial, final)

                        # empty = continue looping
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)

                        # has enemy piece = add move + break
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)
                            break

                        # has team piece = break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    
                    # not in range
                    else: break

                    # incrementing incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            possible_moves = [
                (row-1, col+0), # up
                (row-1, col+1), # up-right
                (row+0, col+1), # right
                (row+1, col+1), # down-right
                (row+1, col+0), # down
                (row+1, col-1), # down-left
                (row+0, col-1), # left
                (row-1, col-1), # up-left
            ]

            # normal moves
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create squares of the new move
                        initial_p5 = self.squares[row][col].piece
                        final_p5 = self.squares[possible_move_row][possible_move_col].piece
                        initial = Square(row, col, initial_p5)
                        final = Square(possible_move_row, possible_move_col, final_p5) # piece=piece
                        # create new move
                        move = Move(initial, final)
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)

            # castling moves
            if not piece.moved:
                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[row][c].has_piece():
                                break
                            
                            # check valid castling
                            initial = Square(row, col)
                            final = Square(row, c) 
                            # create new move
                            move = Move(initial, final)
                            if self.in_check(piece, move):
                                break
                            
                            if c == 3:
                                # adds left rook to king
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)

                                # king move
                                initial_p6 = self.squares[row][col].piece
                                final_p6 = self.squares[row][2].piece
                                initial = Square(row, col, initial_p6)
                                final = Square(row, 2, final_p6)
                                moveK = Move(initial, final)

                                # check potencial checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        # append new move to rook
                                        left_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    left_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)

                # king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[row][c].has_piece():
                                break

                            # check valid castling
                            initial = Square(row, col)
                            final = Square(row, c) 
                            # create new move
                            move = Move(initial, final)
                            if self.in_check(piece, move):
                                break

                            if c == 6:
                                # adds right rook to king
                                piece.right_rook = right_rook

                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                # king move
                                initial_p7 = self.squares[row][col].piece
                                final_p7 = self.squares[row][6].piece
                                initial = Square(row, col, initial_p7)
                                final = Square(row, 6, final_p7)
                                moveK = Move(initial, final)

                                # check potencial checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        # append new move to rook
                                        right_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    right_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)

        if isinstance(piece, Pawn): 
            pawn_moves()

        elif isinstance(piece, Knight): 
            knight_moves()

        elif isinstance(piece, Bishop): 
            straightline_moves([
                (-1, 1), 
                (-1, -1), 
                (1, 1), 
                (1, -1),
            ])

        elif isinstance(piece, Rook): 
            straightline_moves([
                (-1, 0),
                (0, 1),
                (1, 0), 
                (0, -1),
            ])

        elif isinstance(piece, Queen): 
            straightline_moves([
                (-1, 1), 
                (-1, -1), 
                (1, 1), 
                (1, -1), 
                (-1, 0), 
                (0, 1),
                (1, 0), 
                (0, -1)
            ])

        elif isinstance(piece, King): 
            king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == WHITE_PIECE else (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))
        
    def findWhiteKing(self):
        for row in range(ROWS):
            for col in range(COLS):
                square = self.board.squares[row][col]
                if square.has_piece():
                    piece = square.piece
                    if isinstance(piece, King) and piece.color == WHITE_PIECE:
                        return square
                    
    def findBlackKing(self):
        for row in ROWS:
            for col in COLS:
                square = self.board.squares[row][col]
                if square.has_piece():
                    piece = square.piece
                    if isinstance(piece, King) and piece.color == BLACK_PIECE:
                        return square
                    
    def update_castling_rights(self, color, piece, initial, final):
        """Cập nhật quyền nhập thành khi quân cờ di chuyển (đặc biệt là Vua và Xe)"""
        if isinstance(piece, King):
            # Nếu quân Vua di chuyển, loại bỏ quyền nhập thành
            if color == WHITE_PIECE:
                self.castling[WHITE_PIECE] = 0  # Loại bỏ quyền nhập thành của quân trắng
            else:
                self.castling[BLACK_PIECE] = 0  # Loại bỏ quyền nhập thành của quân đen
        elif isinstance(piece, Rook):
            # Nếu quân Xe di chuyển, loại bỏ quyền nhập thành tương ứng
            if color == WHITE_PIECE:
                if initial.col == 0:  # Xe bên trái
                    self.castling[WHITE_PIECE] &= 0b10  # Loại bỏ quyền nhập thành queenside
                elif initial.col == 7:  # Xe bên phải
                    self.castling[WHITE_PIECE] &= 0b01  # Loại bỏ quyền nhập thành kingside
            else:
                if initial.col == 0:  # Xe bên trái
                    self.castling[BLACK_PIECE] &= 0b10  # Loại bỏ quyền nhập thành queenside
                elif initial.col == 7:  # Xe bên phải
                    self.castling[BLACK_PIECE] &= 0b01  # Loại bỏ quyền nhập thành kingside
                    
    def can_castle(self, color, kingside=True):
        """Kiểm tra quyền nhập thành của quân Vua cho một bên (quân trắng hoặc đen)"""
        kside = W_OO if color == WHITE_PIECE else B_OO
        qside = W_OOO if color == WHITE_PIECE else B_OOO

        if kingside:
            return bool(self.castling[color] & kside)
        else:
            return bool(self.castling[color] & qside)
        
        
    # ============================AI==============================
        
        
    def undo_move(self, move):
        if move is None:
            return  # Không có nước đi nào để hoàn tác

        initial = move.initial
        final = move.final
        moved_piece = self.squares[final.row][final.col].piece

        if move.enpassant_captured_piece_row is None:
            # Khôi phục quân cờ về vị trí ban đầu
            self.squares[initial.row][initial.col].piece = moved_piece
            self.squares[final.row][final.col].piece = move.captured_piece  # Khôi phục quân cờ bị ăn (nếu có)
        else:
            # Khôi phục quân enpassant
            self.squares[initial.row][initial.col].piece = moved_piece
            self.squares[final.row][final.col].piece = None
            self.squares[move.enpassant_captured_piece_row][move.enpassant_captured_piece_col].piece = move.captured_piece

        # Hoàn tác phong cấp tốt (nếu có)
        if move.promoted_from is not None:
            self.squares[initial.row][initial.col].piece = move.promoted_from  # Trả lại tốt ban đầu

        # Hoàn tác nhập thành (castling)
        if isinstance(moved_piece, King) and abs(final.col - initial.col) == 2:
            if final.col > initial.col:  # Nhập thành cánh vua
                rook_initial_col, rook_final_col = 7, 5
            else:  # Nhập thành cánh hậu
                rook_initial_col, rook_final_col = 0, 3
            print(final.col, initial.col)
            print(rook_initial_col, rook_final_col)
            rook = self.squares[initial.row][rook_final_col].piece
            print("Rook: ", rook)
            self.squares[initial.row][rook_initial_col].piece = rook  # Đưa xe về vị trí ban đầu
            self.squares[initial.row][rook_final_col].piece = None  # Xóa xe khỏi vị trí mới
            
            self.squares[initial.row][rook_initial_col].piece.moved -=1
            self.delete_nearestMove()

        # Hoàn tác trạng thái di chuyển của quân cờ
        moved_piece.moved -=1
        self.delete_nearestMove()
        
    def to_fen(self, next_player='w', halfmove_clock=0, fullmove_number=1):
        piece_map = {
            'pawn': 'P',
            'knight': 'N',
            'bishop': 'B',
            'rook': 'R',
            'queen': 'Q',
            'king': 'K'
        }

        rows = []
        for row in self.squares:
            fen_row = ''
            empty = 0
            for square in row:
                piece = square.piece
                if not piece:
                    empty += 1
                else:
                    if empty:
                        fen_row += str(empty)
                        empty = 0
                    symbol = piece_map.get(piece.name, '?')
                    fen_row += symbol if piece.color == WHITE_PIECE else symbol.lower()
            if empty:
                fen_row += str(empty)
            rows.append(fen_row)

        board_part = '/'.join(rows)

        # === Castling rights ===
        castling = ''
        if self.squares[7][4].piece and self.squares[7][4].piece.name == 'king' and not self.squares[7][4].piece.moved:
            if self.squares[7][7].piece and self.squares[7][7].piece.name == 'rook' and not self.squares[7][7].piece.moved:
                castling += 'K'
            if self.squares[7][0].piece and self.squares[7][0].piece.name == 'rook' and not self.squares[7][0].piece.moved:
                castling += 'Q'
        if self.squares[0][4].piece and self.squares[0][4].piece.name == 'king' and not self.squares[0][4].piece.moved:
            if self.squares[0][7].piece and self.squares[0][7].piece.name == 'rook' and not self.squares[0][7].piece.moved:
                castling += 'k'
            if self.squares[0][0].piece and self.squares[0][0].piece.name == 'rook' and not self.squares[0][0].piece.moved:
                castling += 'q'
        if not castling:
            castling = '-'

        # === En Passant Target ===
        en_passant = '-'
        last_move = self.getLastestMove() if hasattr(self, 'getLastestMove') else None
        if last_move:
            piece = last_move.initial.piece
            if piece and piece.name == 'pawn':
                start_row = last_move.initial.row
                end_row = last_move.final.row
                # Check if it was a 2-step pawn move
                if abs(start_row - end_row) == 2:
                    target_row = (start_row + end_row) // 2
                    target_col = last_move.initial.col
                    en_passant = Square.get_alphacol(target_col) + str(8 - target_row)

        return f"{board_part} {next_player} {castling} {en_passant} {halfmove_clock} {fullmove_number}"