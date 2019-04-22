import numpy as np

class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valids = self.game.getValidMoves(board, 1).flatten()
        nonzero = np.nonzero(valids)
        rand_ind = np.random.randint(len(nonzero))
        move = nonzero[0][rand_ind]
        return move

