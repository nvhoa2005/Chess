class PGNBuilder:
        def __init__(self):
            self.moves = []

        def add_move(self, move, piece, is_capture=False, is_check=False, is_checkmate=False, is_castling=False):
            notation = ""

            if is_castling:
                # Castling notation
                if move.final.col == 6:
                    notation = "O-O"
                elif move.final.col == 2:
                    notation = "O-O-O"
            else:
                # Piece abbreviation
                piece_symbol = "" if piece.name == "pawn" else piece.name[0].upper()

                # Pawn capture notation includes file of departure
                if piece.name == "pawn" and is_capture:
                    piece_symbol = move.initial.alphacol

                capture_symbol = "x" if is_capture else ""

                dest = f"{move.final.alphacol}{8 - move.final.row}"

                notation = f"{piece_symbol}{capture_symbol}{dest}"

                if is_checkmate:
                    notation += "#"
                elif is_check:
                    notation += "+"

            self.moves.append(notation)

        def get_pgn(self):
            pgn = ""
            for i in range(0, len(self.moves), 2):
                move_number = (i // 2) + 1
                white_move = self.moves[i]
                black_move = self.moves[i + 1] if i + 1 < len(self.moves) else ""
                pgn += f"{move_number}. {white_move} {black_move} "
            return pgn.strip()

        def reset(self):
            self.moves = []
