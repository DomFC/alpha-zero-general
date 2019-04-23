import numpy as np
from .Board import Board
from .Board import _1D_to_2D_board, _1D_to_2D_coord, DIRECTIONS, MOVE_LEN
from .CheckersLogic import CheckersLogic

from string import ascii_uppercase

DIM = 8
coordinates_list = list(ascii_uppercase)[:DIM]

class HumanPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valids = self.game.getValidMoves(board, 1)
        for move_ind, move in enumerate(valids):
            if move == 0:
                continue
            coord, direction, move_len = CheckersLogic.get_move_values(move_ind)
            row_i, col_i = _1D_to_2D_coord(coord)
            row_f = row_i + DIRECTIONS[direction][0] * MOVE_LEN[move_len]
            col_f = col_i + DIRECTIONS[direction][1] * MOVE_LEN[move_len]
            play = [
                    [coordinates_list[row_i], coordinates_list[col_i]],
                    [coordinates_list[row_f], coordinates_list[col_f]]
                   ]
            print(play, 'input', move_ind)
        while True:
            play = int(input().strip().replace(' ', ''))
            if valids[play] == 1:
                return play
            print('move is invalid')
