import Arena
import checkers_terminal
from MCTS import MCTS
from checkers.CheckersGame import CheckersGame
from checkers.HumanPlayer import HumanPlayer
from checkers.pytorch.NNet import NNetWrapper as NNet
from checkers.Board import _1D_to_2D_board


import numpy as np
from utils import *

print('Who starts? [h/n]')
starting = input().strip()

g = CheckersGame()

hp = HumanPlayer(g).play

# nnet player
n1 = NNet(g)
n1.load_checkpoint('./pretrained_models/','residual_20.pth.tar')
args1 = dotdict({'numMCTSSims': 40, 'cpuct':0.0001})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

players = [hp, n1p]
if starting != 'h':
    players = [n1p, hp]

arena = Arena.Arena(players[0], players[1], g, display=checkers_terminal.display)
print('Wins, Losses, Draws =', arena.playGames(1000, verbose=True))
