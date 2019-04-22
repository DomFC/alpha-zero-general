import Arena
import checkers_terminal
from MCTS import MCTS
from checkers.CheckersGame import CheckersGame
from checkers.RandomPlayer import RandomPlayer
from checkers.pytorch.NNet import NNetWrapper as NNet
from checkers.Board import _1D_to_2D_board


import numpy as np
from utils import *

g = CheckersGame()

rp = RandomPlayer(g).play

# nnet players
n1 = NNet(g)
n1.load_checkpoint('./pretrained_models/checkers/domfc/','best.pth.tar')
args1 = dotdict({'numMCTSSims': 3, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

arena = Arena.Arena(n1p, rp, g, display=checkers_terminal.display)
print('Wins, Losses, Draws =', arena.playGames(1000, verbose=True))
