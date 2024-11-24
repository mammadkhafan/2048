from Game import Game2048
from Graphic import Game2048GUI

game = Game2048(4, 4)
graphic = Game2048GUI(game)
graphic.run()