import copy
from .Piece import Piece
DIM = 8

class CheckersLogic():
    def apply_move(board, turn, row_i, col_i, row_f, col_f):
        capture = False
        moving_piece = board[row_i, col_i]

        # Step
        if abs(row_f - row_i) == 1:
            board[row_i, col_i] = Piece.NONE
            board[row_f, col_f] = moving_piece
        # Capture
        elif abs(row_f - row_i) == 2:
            die_row, die_col = row_i + (row_f - row_i) // 2, col_i + (col_f - col_i) // 2
            board[row_i, col_i] = Piece.NONE
            board[die_row, die_col] = Piece.NONE
            board[row_f, col_f] = moving_piece
            capture = True

        # Change piece to king if it reached the other side
        end_row = DIM - 1 if turn == Piece.BLACK else 0
        if row_f == end_row and abs(board[row_f, col_f]) == 1:
            board[row_f, col_f] *= 2

        return capture

    def valid_move(board, turn, row_i, col_i, row_f, col_f, mid_capture):
        # Move is invalid if any coordinates is negative or too large
        for x in [row_i, col_i, row_f, col_f]:
            if x < 0 or x >= DIM:
                return False

        # Move is invalid by any other piece if a piece is mid-capture
        if mid_capture is not None:
            if row_i != mid_capture[0] or col_i != mid_capture[1]:
                return False

        moving_piece = board[row_i, col_i]

        # Check if position has a piece
        if moving_piece == Piece.NONE:
            return False

        # Refuse play if wrong color is moving
        if moving_piece / abs(moving_piece) != turn:
            return False

        # Set direction
        direction = None if abs(moving_piece) == 2 else 1
        if direction is not None:
            direction *= 1 if turn == Piece.BLACK else -1


        # Check the direction on non-kings
        if direction is not None:
            if direction * (row_f - row_i) <= 0:
                return False

        # Check if move is diagonal
        delta_row, delta_col = row_f - row_i, col_f - col_i
        if abs(delta_row) != abs(delta_col):
            return False

        # Check step
        # It is assumed that capture is not mandatory in this case, this is applied in another function
        if abs(delta_row) == 1:
            # Cant step if it's not the first movement of the move
            if mid_capture is not None:
                return False
            # Destination must be empty
            if board[row_f, col_f] != 0:
                return False
        # Check for a capture
        elif abs(delta_row) == 2:
            # Destination must be empty
            if board[row_f, col_f] != 0:
                return False
            # Check for a captured piece
            opponent = -turn
            die_row, die_col = row_i + delta_row // 2, col_i + delta_col // 2
            jumped_over = board[die_row, die_col]
            if jumped_over == 0 or jumped_over // abs(jumped_over) != opponent:
                return False
        # Move is too far
        else:
            return False
        # The move is valid is all of the above is respected
        return True

    def get_move_values(move):
        if move < 0 or move > 255:
            return None

        coord = move // 8
        direction = (move % 8) // 2
        move_len = move % 2

        return coord, direction, move_len