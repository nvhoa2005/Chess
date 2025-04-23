import clr
import os
from move import Move as PyMove  # Your Python Move class
from square import Square  # Your Square class

# Load the ChessLib DLL
dll_path = os.path.join(os.path.dirname(__file__), "ChessLib2.dll")
clr.AddReference(dll_path)

# Import the ChessLib types
from ChessLib import Search2, Board, Move as CsMove


def convert_cs_move_to_py_move(cs_move):
    """
    Converts a C# Move (from ChessLib) to a Python Move instance.
    This conversion creates Square objects for the initial and final positions.

    Parameters:
        cs_move: The C# Move instance.

    Returns:
        A Python Move instance with initial and final squares as Square objects.
    """
    # Extract the square indices from the C# move.
    start_index = cs_move.StartSquare  # integer 0-63
    target_index = cs_move.TargetSquare

    # Convert the index to row and col.
    # Assuming index 0 = row 0, col 0, where row = index // 8 and col = index % 8.
    start_row = 7 - (start_index // 8)
    start_col = start_index % 8
    
    target_row = 7 - (target_index // 8)
    target_col = target_index % 8

    # Create Square objects (with no piece info provided).
    initial_square = Square(start_row, start_col)
    final_square = Square(target_row, target_col)

    # Create and return a Python Move instance.
    return PyMove(initial_square, final_square)


# Example usage:
# fenn = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
# board = Board()
# board.LoadPosition(fenn)
# searcher = Search2(board)
# time = 1000
#
# cs_move = searcher.getBestMove(time)
# py_move = convert_cs_move_to_py_move(cs_move)
#
# print("C# Move Name:", cs_move.Name)
# print("Converted Python Move:")
# print("Initial square:", py_move.initial.row, py_move.initial.col)
# print("Final square:", py_move.final.row, py_move.final.col)
