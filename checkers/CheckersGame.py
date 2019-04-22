import sys
from .Piece import Piece
from .Board import Board, _mirror_action
#sys.path.append('..')
from Game import Game
import numpy as np
import copy

W = 4
H = 8

class CheckersGame(Game):
    def __init__(self):
        pass

    def getInitBoard(self):
        return Board()

    def getBoardSize(self):
        return (W, H)

    def getActionSize(self):
        return W * H * 4 * 2

    def getNextState(self, board, player, action):
        if board.flipped_board:
            action = _mirror_action(action)
        next_board = copy.deepcopy(board)
        next_turn = next_board.play_move(player, action)
        return next_board, next_turn

    def getValidMoves(self, board, player):
        return board.get_valid_moves(player).flatten()

    def getGameEnded(self, board, player):
        return board.winner(player)

    def getCanonicalForm(self, board, player):
        # If the player is white, return the board unchanged, otherwise flip it.
        if player == Piece.WHITE:
            if board.flipped_board:
                return board.flipped()
            return board
        else:
            if board.flipped_board:
                return board
            return board.flipped()

    def getSymmetries(self, board, pi):
        return [(board, pi)]

    def stringRepresentation(self, board):
        return str(board.tostring()) + str(board.mid_capture) + str(board.flipped_board)

