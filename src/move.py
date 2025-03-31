class Move:
    def __init__(self, initial, final, captured_piece=None, promoted_from=None, enpassant_captured_piece_prev_row=None, enpassant_captured_piece_prev_col=None, enpassant_captured_piece_row=None, enpassant_captured_piece_col=None):
        self.initial = initial
        self.final = final
        self.captured_piece = captured_piece
        self.promoted_from = promoted_from
        self.enpassant_captured_piece_row = enpassant_captured_piece_row
        self.enpassant_captured_piece_col = enpassant_captured_piece_col
        self.enpassant_captured_piece_prev_row = enpassant_captured_piece_prev_row
        self.enpassant_captured_piece_prev_col = enpassant_captured_piece_prev_col

    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final
