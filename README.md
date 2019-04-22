# Alpha Zero General pour le jeu de Dames
Ce "fork" de Alpha Zero General a été fait dans le contexte du projet final du cours INF8225. L'objectif est d'appliquer la méthode utilisée par AlphaGo sur le jeu de Dames. Les résultats de ce projet sont détaillés dans le rapport remis.

Les scripts suivants sont utiles pour faire des expériences:
* ```main.py```: Ce script lance l'entraînement d'un réseau. Les hyperparamètres peuvent être ajustés dans la variable ```args``` et le type de réseau (conv, res) peut être changé dans le répertoire ```checkers/pytorch/NNet.py```. Il est a noté que certaines combinaisons d'hyperparamètres peuvent ne pas fonctionner, par exemple si un modèle non-existant est donné comme base ou si la mémoire dédiée d'un GPU supportant CUDA est excédée.
* ```checkers_random.py```: Ce script fait joueur un modèle contre un joueur aléatoire. Des paramètres comme le nombre de simulations MCTS, la verbosité et le nombre de parties doivent être ajsutés dans ce fichier.
* ```checkers_human.py```: Ce script fait joueur un modèle contre un joueur humain  travers une interface console. Des paramètres comme le nombre de simulations MCTS, la verbosité et le nombre de parties doivent être ajustés dans ce fichier.

Les réseaux préentrainés peuvent être récupérés dans ce dossier : https://drive.google.com/open?id=1LFseByaJBhiCbOOon3zpIijLNdvSgUGE

Il est à noté que tenter de charger un réseau avec la mauvaise configuration ne fonctionnera pas. Il faut utiliser le bon réseau dans le fichier ```checkers/pytorch/NNet.py```.


Le README original est inclu ci-dessous.
# Alpha Zero General (any game, any framework!)

A simplified, highly flexible, commented and (hopefully) easy to understand implementation of self-play based reinforcement learning based on the AlphaGo Zero paper (Silver et al). It is designed to be easy to adopt for any two-player turn-based adversarial game and any deep learning framework of your choice. A sample implementation has been provided for the game of Othello in PyTorch, Keras, TensorFlow and Chainer. An accompanying tutorial can be found [here](http://web.stanford.edu/~surag/posts/alphazero.html). We also have implementations for GoBang and TicTacToe.

To use a game of your choice, subclass the classes in ```Game.py``` and ```NeuralNet.py``` and implement their functions. Example implementations for Othello can be found in ```othello/OthelloGame.py``` and ```othello/{pytorch,keras,tensorflow,chainer}/NNet.py```. 

```Coach.py``` contains the core training loop and ```MCTS.py``` performs the Monte Carlo Tree Search. The parameters for the self-play can be specified in ```main.py```. Additional neural network parameters are in ```othello/{pytorch,keras,tensorflow,chainer}/NNet.py``` (cuda flag, batch size, epochs, learning rate etc.). 

To start training a model for Othello:
```bash
python main.py
```
Choose your framework and game in ```main.py```.

### Docker Installation
For easy environment setup, we can use [nvidia-docker](https://github.com/NVIDIA/nvidia-docker). Once you have nvidia-docker set up, we can then simply run:
```
./setup_env.sh
```
to set up a (default: pyTorch) Jupyter docker container. We can now open a new terminal and enter:
```
docker exec -ti pytorch_notebook python main.py
```

### Experiments
We trained a PyTorch model for 6x6 Othello (~80 iterations, 100 episodes per iteration and 25 MCTS simulations per turn). This took about 3 days on an NVIDIA Tesla K80. The pretrained model (PyTorch) can be found in ```pretrained_models/othello/pytorch/```. You can play a game against it using ```pit.py```. Below is the performance of the model against a random and a greedy baseline with the number of iterations.
![alt tag](https://github.com/suragnair/alpha-zero-general/raw/master/pretrained_models/6x6.png)

A concise description of our algorithm can be found [here](https://github.com/suragnair/alpha-zero-general/raw/master/pretrained_models/writeup.pdf).

### Contributing
While the current code is fairly functional, we could benefit from the following contributions:
* Game logic files for more games that follow the specifications in ```Game.py```, along with their neural networks
* Neural networks in other frameworks
* Pre-trained models for different game configurations
* An asynchronous version of the code- parallel processes for self-play, neural net training and model comparison. 
* Asynchronous MCTS as described in the paper

### Contributors and Credits
* [Shantanu Thakoor](https://github.com/ShantanuThakoor) and [Megha Jhunjhunwala](https://github.com/jjw-megha) helped with core design and implementation.
* [Shantanu Kumar](https://github.com/SourKream) contributed TensorFlow and Keras models for Othello.
* [Evgeny Tyurin](https://github.com/evg-tyurin) contributed rules and a trained model for TicTacToe.
* [MBoss](https://github.com/1424667164) contributed rules and a model for GoBang.
* [Jernej Habjan](https://github.com/JernejHabjan) contributed RTS game.

Thanks to [pytorch-classification](https://github.com/bearpaw/pytorch-classification) and [progress](https://github.com/verigak/progress).

