import random
from board import Board
from move import Move
from piece import *
from const import *
from eval import evaluateComplete

class AIEngine:

    def __init__(self, board, game):
        self.board = board
        self.game = game

    def evaluate_board(self):
        """
        Đánh giá bàn cờ dựa trên hàm đánh giá chi tiết từ eval.py
        """
        color = self.game.next_player
        return evaluateComplete(self.game, color)

    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        """
        Cải tiến Alpha-Beta Pruning để tối ưu AI.
        """
        if depth == 0 or self.is_checkmate():
            return self.evaluate_board()
        
        moves = self.get_all_moves(BLACK_PLAYER if maximizing_player else WHITE_PLAYER)
        
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
        
        moves = self.get_all_moves(BLACK_PLAYER)
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
            check_promotion = list()
            self.board.move(piece, move, promotion=check_promotion)
            self.board.update_castling_rights(piece.color, piece, move.initial, move.final)
            self.game.show_bg(screen)
            self.game.show_last_move(screen)
            self.game.show_pieces(screen)
            # check promotion
            if len(check_promotion) > 0:
                self.board.squares[move.final.row][move.final.col].piece = Queen(piece.color)
            
            c = 0
            # check is_checkmate
            if self.game.is_checkmate():
                winner = WHITE_WIN if self.next_player == WHITE_PLAYER else BLACK_WIN
                self.paused = True
                c = self.display_paused_game(screen, winner)
                
            # check draw
            if self.game.is_draw():
                winner = DRAW
                self.game.paused = True
                c = self.display_paused_game(screen, winner)
                
            # next turn
            if c != RESTART:
                self.game.next_turn()
        # else:
        #     # Kiểm tra nếu AI bị chiếu hết hoặc hòa
        #     if self.game.is_checkmate():
        #         print("Checkmate! Người chơi thắng!")
        #     else:
        #         print("AI không thể di chuyển, ván cờ kết thúc.")
                
    def is_checkmate(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_enemy_piece(self.game.next_player):
                    piece = self.board.squares[row][col].piece
                    self.board.calc_moves(piece, row, col)
                    if len(piece.moves) != 0:
                        return False
        return True
