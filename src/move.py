class Move:
    def __init__(self, initial, final, captured_piece=None, promoted_from=None):
        self.initial = initial
        self.final = final
        self.captured_piece = captured_piece  # Quân cờ bị ăn (nếu có)
        self.promoted_from = promoted_from  # Lưu lại tốt nếu nó được phong cấp

    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final
