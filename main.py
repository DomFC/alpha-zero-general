from Coach import Coach
from Plots import Plots
from checkers.CheckersGame import CheckersGame as Game
#from othello.OthelloGame import OthelloGame as Game
#from othello.pytorch.NNet import NNetWrapper as nn
from checkers.pytorch.NNet import NNetWrapper as nn
from checkers.pytorch.NNet import args as nnet_args
from utils import *

args = dotdict({
    'numIters': 0,
    'numEps': 10,
    'tempThreshold': 15,
    'updateThreshold': 0.42,
    'maxlenOfQueue': 20000,
    'numMCTSSims': 3,
    'arenaCompare': 40,
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})

if __name__=="__main__":
    g = Game()
    nnet = nn(g)

    if args.load_model:
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

    c = Coach(g, nnet, args)
    if args.load_model:
        print("Load trainExamples from file")
        c.loadTrainExamples()
    c.learn()
    plots = Plots()
    plots.show_experiment(c.pi_losses, c.v_losses, nnet_args, args)
