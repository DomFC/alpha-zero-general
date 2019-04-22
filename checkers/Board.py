import copy
from .Piece import Piece
from .CheckersLogic import CheckersLogic
import numpy as np

W = 4
H = 8

DIRECTIONS = [
    [1, 1],
    [1, -1],
    [-1, -1],
    [-1, 1],
]

MOVE_LEN = [1, 2]

class Board(np.ndarray):
    def __new__(subtype, shape=(H*W), dtype=int, buffer=None, offset=0,
                strides=None, order=None, mid_capture=None):
        obj = super(Board, subtype).__new__(subtype, shape, dtype,
                                                buffer, offset, strides,
                                                order)
        obj.mid_capture = mid_capture
        obj.moves_since_capture = 0
        obj.flipped_board = False
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self.mid_capture = getattr(obj, 'mid_capture', None)
        self.moves_since_capture = getattr(obj, 'moves_since_capture', None)
        self.flipped_board = getattr(obj, 'flipped_board', None)

    def __init__(self):
        _initial_state(self)

    def flipped(self):
        new_board = copy.deepcopy(self)
        for i in range(16):
            new_board[i], new_board[31 - i] = -new_board[31 - i], -new_board[i]
        new_board.flipped_board ^= True
        new_board.mid_capture = None if not new_board.mid_capture else (7 - new_board.mid_capture[0], 7 - new_board.mid_capture[1])
        return new_board

    def get_valid_moves(self, turn):
        tmp_board = _1D_to_2D_board(self)

        valid_moves = np.zeros((W*H, 4, 2))
        found_valid_capture = False
        m_c = self.mid_capture
        for coord in range(32):
            for dir_ind, direction in enumerate(DIRECTIONS):
                for move_len_ind, move_len in enumerate(MOVE_LEN):
                    row_i, col_i = _1D_to_2D_coord(coord)
                    row_f, col_f = row_i + direction[0] * move_len, col_i + direction[1] * move_len
                    if CheckersLogic.valid_move(tmp_board, turn, row_i, col_i, row_f, col_f, m_c):
                        if self.flipped_board:
                            new_coord = 31 - coord
                            new_dir_ind = (dir_ind + 2) % 4
                            new_move_len_ind = move_len_ind
                            valid_moves[new_coord, new_dir_ind, new_move_len_ind] = 1
                        else:
                            valid_moves[coord, dir_ind, move_len_ind] = 1
                        if move_len == 2:
                            found_valid_capture = True

        # A capture was found, remove all simple steps
        if found_valid_capture:
            valid_moves[:, :, 0] = 0

        return valid_moves.flatten()

    def play_move(self, turn, move):
        tmp_board = _1D_to_2D_board(self)

        #if self.flipped_board or turn == -1:
        #    move = _mirror_action(move)
            #tmp_board = tmp_board.flipped()

        row_i, col_i = _1D_to_2D_coord(move // 8)
        direction = (move % 8) // 2
        move_len = (move % 2) + 1

        row_f = row_i + DIRECTIONS[direction][0] * move_len
        col_f = col_i + DIRECTIONS[direction][1] * move_len

        assert CheckersLogic.valid_move(tmp_board, turn, row_i, col_i, row_f, col_f, self.mid_capture),\
                "Valid move assertion failed. \nBoard:\n{}\n, Turn:\n{}\n, row_i, col_i:\n{}\n, row_f,col_f:\n{}\n, mid:\n{}\nFlip:{}\n".\
                format(tmp_board, turn, (row_i, col_i), (row_f, col_f), self.mid_capture, self.flipped_board)

        just_captured = CheckersLogic.apply_move(tmp_board, turn, row_i, col_i, row_f, col_f)

        tmp_board = _2D_to_1D_board(tmp_board)
        for i in range(32):
            self[i] = tmp_board[i]

        # If we captured, we check if another capture might be possible later,
        # otherwise we give the turn
        new_turn = copy.deepcopy(turn)
        if just_captured:
            self.moves_since_capture = 0
            self.mid_capture = (row_f, col_f)
            if np.count_nonzero(self.get_valid_moves(turn).flatten()) == 0:
                new_turn *= -1
                self.mid_capture = None
        else:
            self.moves_since_capture += 1
            new_turn *= -1

        return new_turn

    def winner(self, turn):
        if np.count_nonzero(self.get_valid_moves(turn)) == 0:
            return -1
        b = 0
        w = 0
        for coord in range(32):
            if self[coord] > 0:
                w += 1
            elif self[coord] < 0:
                b += 1
        if b == 0:
            return 1 if turn == Piece.WHITE else -1
        if w == 0:
            return 1 if turn == Piece.BLACK else -1
        if self.moves_since_capture >= 50:
            return -0.5
        return 0


def _1D_to_2D_coord(coord):
    if coord is None:
        return None
    row = coord // 4
    col = (1 if coord % 8 < 4 else 0) + (coord % 4) * 2
    return row, col

def _2D_to_1D_coord(row, col):
    if (row + col) % 2 == 0:
        return None
    col //= 2
    return row * 4 + col

def _initial_state(state):
    for i in range(12):
        state[i] = Piece.BLACK
    for i in range(12,20):
        state[i] = Piece.NONE
    for i in range(20, 32):
        state[i] = Piece.WHITE

def _1D_to_2D_board(board):
    new_board = np.zeros((8, 8))
    for i in range(32):
        row, col = _1D_to_2D_coord(i)
        new_board[row, col] = board[i]
    return new_board

def _2D_to_1D_board(board):
    new_board = np.zeros((32))
    for coord in range(32):
        row, col = _1D_to_2D_coord(coord)
        new_board[coord] = board[row, col]

    return new_board

def _mirror_action(action):
    coord = action // 8
    direction = (action % 8) // 2
    move_len = (action % 2)
    coord = 31 - coord
    direction = (direction + 2) % 4
    return 8 * coord + 2 * direction + move_len
